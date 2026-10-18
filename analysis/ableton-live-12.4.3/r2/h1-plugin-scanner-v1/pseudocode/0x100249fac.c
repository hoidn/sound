
void FUN_100249fac(undefined8 param_1)

{
  FUN_1002170ac(param_1,
                "CREATE TABLE plugin_modules (   module_id      INTEGER PRIMARY KEY,   path           TEXT,   arch           INTEGER DEFAULT 0,   scanstate      INTEGER DEFAULT 0 ); "
               );
  FUN_1002170ac(param_1,
                "CREATE TABLE plugin_domains (   id             TEXT,   module_id      INTEGER DEFAULT 0,   enabled        INTEGER DEFAULT 0 ); "
               );
  FUN_1002170ac(param_1,
                "CREATE TABLE plugins (   plugin_id      INTEGER PRIMARY KEY,   module_id      INTEGER DEFAULT 0,   dev_identifier TEXT,   name           TEXT,   vendor         TEXT,   version        TEXT,   device_type    TEXT,   scanstate      INTEGER DEFAULT 0,   enabled        INTEGER DEFAULT 0 ); "
               );
  return;
}

