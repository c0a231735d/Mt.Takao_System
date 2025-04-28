-- init_db.sql
CREATE TABLE IF NOT EXISTS stamps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(255) NOT NULL,
    qr_code VARCHAR(255) NOT NULL
);

ALTER TABLE stamps ADD COLUMN is_peak BOOLEAN DEFAULT FALSE;

INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートA', 'QR_CODE_A2', TRUE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B1', FALSE);
INSERT INTO stamps (route_name, qr_code, is_peak) VALUES ('ルートB', 'QR_CODE_B2', TRUE);