from enum import Enum

class TipoCampo(Enum):
    VARCHAR = 'VARCHAR'
    BINARY = 'BINARY'
    VARBINARY = 'VARBINARY'
    TINYBLOB = 'TINYBLOB'
    TINYTEXT = 'TINYTEXT'
    TEXT = 'TEXT'
    BLOB = 'BLOB'
    MEDIUMTEXT = 'MEDIUMTEXT'
    MEDIUMBLOB = 'MEDIUMBLOB'
    LONGTEXT = 'LONGTEXT'
    LONGBLOG = 'LONGBLOG'
    ENUM = 'ENUM'
    SET = 'SET'
    BIT = 'BIT'
    TINYINT = 'TINYINT'
    BOOL = 'BOOL'
    BOOLEAN = 'BOOLEAN'
    SMALLINT = 'SMALLINT'
    MEDIUMINT = 'MEDIUMINT'
    INT = 'INT'
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    DECIMAL = 'DECIMAL'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIME = 'TIME'
    YEAR = 'YEAR'