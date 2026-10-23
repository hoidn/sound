"""Exploratory raw-audio spectrum only; no source execution or acceptance oracle."""
import json
import math
from pathlib import Path
import sys

import numpy as np

FS = 44100
FRAMES = 16384
WINDOWS = ((4096, 16384), (4096, 10240), (10240, 16384))
HYPOTHESES = (261.62, 523.24)
HALF_BAND_HZ = 20.0
PAD_FACTOR = 8
TOP_PEAKS = 8


def decode(raw):
    if len(raw) != FRAMES * 2 * 4:
        raise ValueError("exactly 16384 interleaved stereo little-endian f32 frames required")
    values = np.frombuffer(raw, dtype="<f4").reshape(FRAMES, 2).astype(np.float64)
    if not np.isfinite(values).all():
        raise ValueError("all samples, including prefix, must be finite")
    return values


def describe(raw):
    values = decode(raw)
    result = {
        "status": "diagnostic-only", "fs_hz": FS, "frames": FRAMES,
        "method": "Raw values, symmetric np.hanning, real FFT padded to 8*N; no detrending, fitting or alignment.",
        "magnitude": "2*abs(FFT)/sum(Hann), with DC/Nyquist not doubled; a spectral-bin magnitude, not calibrated component amplitude.",
        "hypothesis_bands": "Fixed center +/-20Hz; report magnitude evidence, no binary presence/absence decision.",
        "limits": [
            "Largest peak is not identified as fundamental; harmonics, modes and mixtures may dominate.",
            "Padding refines the displayed grid, not independent resolution or an uncertainty bound.",
            "Window duration, Hann leakage, damping, modulation and mixtures limit localization; no CI or calibrated frequency error.",
            "Three windows are descriptive views, not proof of stationarity, full-record invariance or eligibility for another metric.",
            "No note/pitch identity, detector law, acceptance tolerance, compatibility grade or fundamental oracle."
        ],
        "expected": None, "comparison": None, "windows": []
    }
    for start, stop in WINDOWS:
        n = stop - start
        hann = np.hanning(n)
        nfft = n * PAD_FACTOR
        freq = np.fft.rfftfreq(nfft, 1.0 / FS)
        window = {"start_inclusive": start, "stop_exclusive": stop,
                  "samples": n, "duration_seconds": n / FS,
                  "unpadded_bin_hz": FS / n, "padded_grid_hz": FS / nfft,
                  "Hann_approx_main_lobe_null_to_null_hz": 4 * FS / n,
                  "channels": []}
        for channel in (0, 1):
            y = values[start:stop, channel]
            magnitude = np.abs(np.fft.rfft(y * hann, n=nfft)) / hann.sum()
            magnitude[1:-1] *= 2
            maxima = np.flatnonzero((magnitude[1:-1] > magnitude[:-2]) &
                                   (magnitude[1:-1] >= magnitude[2:])) + 1
            maxima = list(map(int, maxima))
            if magnitude[0] > magnitude[1]:
                maxima.append(0)
            if magnitude[-1] > magnitude[-2]:
                maxima.append(len(magnitude) - 1)
            ranked = sorted(maxima, key=lambda i: (-magnitude[i], i))
            strongest = float(magnitude.max())

            def peak(i):
                return {"frequency_hz": float(freq[i]), "bin_magnitude": float(magnitude[i])}

            bands = []
            for center in HYPOTHESES:
                indices = np.flatnonzero((freq >= center - HALF_BAND_HZ) &
                                         (freq <= center + HALF_BAND_HZ))
                best = int(indices[np.argmax(magnitude[indices])])
                nearest = int(np.argmin(np.abs(freq - center)))
                local = [i for i in ranked if center - HALF_BAND_HZ <= freq[i] <= center + HALF_BAND_HZ]
                bands.append({"center_hz": center, "low_hz": center - HALF_BAND_HZ,
                              "high_hz": center + HALF_BAND_HZ, "maximum_grid_bin": peak(best),
                              "nearest_center_grid_bin": peak(nearest),
                              "max_over_strongest_bin": float(magnitude[best] / strongest) if strongest else None,
                              "strongest_local_peaks_in_band": [peak(i) for i in local[:3]]})
            window["channels"].append({"channel": channel,
                                       "raw_rms": math.sqrt(float(np.mean(y * y))),
                                       "nonzero_samples": int(np.count_nonzero(y)),
                                       "strong_local_peaks": [peak(i) for i in ranked[:TOP_PEAKS]],
                                       "bands": bands})
        result["windows"].append(window)
    return result


def self_test():
    t = np.arange(FRAMES - 4096, dtype=np.float64) / FS
    checks = []
    for name, low, high, dominant in (("261.62-tone", 1, 0, 0),
                                      ("523.24-tone", 0, 1, 1),
                                      ("weak-low-strong-harmonic", .05, 1, 1)):
        signal = low * np.sin(2 * np.pi * HYPOTHESES[0] * t) + high * np.sin(2 * np.pi * HYPOTHESES[1] * t)
        values = np.zeros((FRAMES, 2), dtype="<f4")
        values[4096:, :] = signal[:, None]
        diagnostic = describe(values.tobytes())
        for window in diagnostic["windows"]:
            for channel in window["channels"]:
                assert abs(channel["strong_local_peaks"][0]["frequency_hz"] - HYPOTHESES[dominant]) <= window["unpadded_bin_hz"]
                if name == "weak-low-strong-harmonic":
                    assert channel["bands"][0]["maximum_grid_bin"]["bin_magnitude"] > 0
                    assert channel["bands"][1]["maximum_grid_bin"]["bin_magnitude"] > 10 * channel["bands"][0]["maximum_grid_bin"]["bin_magnitude"]
        checks.append(name)
    valid = np.zeros((FRAMES, 2), dtype="<f4").tobytes()
    invalid = bytearray(valid)
    invalid[:4] = np.array([np.nan], dtype="<f4").tobytes()
    for name, raw in (("short", valid[:-4]), ("extra-frame", valid + bytes(8)),
                       ("nonfinite-prefix", bytes(invalid))):
        try:
            describe(raw)
        except ValueError:
            checks.append(name)
        else:
            raise AssertionError(name)
    return {"status": "synthetic-self-check-pass", "checks": checks,
            "limit": "Synthetic frequency assertions test this helper only; no actual-capture threshold or fundamental inference."}


def main():
    if sys.argv[1:] == ["--self-test"]:
        print(json.dumps(self_test(), allow_nan=False))
        return 0
    if len(sys.argv) != 2 or sys.argv[1].startswith("--"):
        print("usage: corpus-midi-spectral-diagnostic.py RAW.f32 | --self-test", file=sys.stderr)
        return 2
    try:
        result = describe(Path(sys.argv[1]).read_bytes())
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "invalid", "error": str(error)}))
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
