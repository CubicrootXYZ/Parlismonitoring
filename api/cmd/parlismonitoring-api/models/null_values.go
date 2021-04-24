package models

import (
    "encoding/json"
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
)


// INTEGER
type NInt struct {
    sql.NullInt64
}

func (v *NInt) MarshalJSON() ([]byte, error) {
    if v.Valid {
        return json.Marshal(v.Int64)
    } else {
        return json.Marshal(nil)
    }
}

func (v *NInt) UnmarshalJSON(data []byte) error {
    // Unmarshalling into a pointer will let us detect null
    var x *int64
    if err := json.Unmarshal(data, &x); err != nil {
        return err
    }
    if x != nil {
        v.Valid = true
        v.Int64 = *x
    } else {
        v.Valid = false
    }
    return nil
}

// STRING
type NString struct {
    sql.NullString
}

func (v *NString) MarshalJSON() ([]byte, error) {
    if v.Valid {
        return json.Marshal(v.String)
    } else {
        return json.Marshal(nil)
    }
}

// TIME
type NTime struct {
    sql.NullTime
}

func (v *NTime) MarshalJSON() ([]byte, error) {
    if v.Valid {
        return json.Marshal(v.Time)
    } else {
        return json.Marshal(nil)
    }
}

// FLOAT
type NFloat struct {
    sql.NullFloat64
}

func (v *NFloat) MarshalJSON() ([]byte, error) {
    if v.Valid {
        return json.Marshal(v.Float64)
    } else {
        return json.Marshal(nil)
    }
}