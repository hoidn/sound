"""Calibrate the independent estimator on analytic tones, without device code."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
p=HERE.with_name('device-analog-v1')/'compare.py'
spec=importlib.util.spec_from_file_location('metric',p);metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric)
rows=[]
for rate in [44100,48000]:
    n=np.arange(rate)/rate
    for center in [130.8,261.6,795.77,2118.569]:
        frequency=center+0.007
        y=(0.7*np.cos(2*np.pi*frequency*n+.3)+0.05*np.sin(2*np.pi*2*frequency*n-.2)+.002).astype(np.float32).astype(float)
        estimate=metric.frequency(y,center,rate)
        amplitudes,dc=metric.harmonic_fit(y,frequency,rate,3)
        assert abs(estimate-frequency)/frequency<1e-7,(rate,center,estimate)
        assert abs(amplitudes[0]-.7)<1e-8 and abs(amplitudes[1]-.05)<1e-8 and amplitudes[2]<1e-8
        assert abs(dc-.002)<1e-8
        rows.append({'rate':rate,'center':center,'relative_frequency_error':abs(estimate-frequency)/frequency,'fundamental_amplitude_error':abs(amplitudes[0]-.7),'second_harmonic_amplitude_error':abs(amplitudes[1]-.05),'dc_error':abs(dc-.002)})
report={'status':'pass','scope':'analytic single-periodic-tone estimator and harmonic/DC recovery only, not device compatibility or arm64 tolerance','cases':rows}
(HERE/'metric-calibration.json').write_text(json.dumps(report,indent=1)+'\n');print('analytic calibration passed',len(rows),'tones; max relative frequency error',max(r['relative_frequency_error'] for r in rows))
