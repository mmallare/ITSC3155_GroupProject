-- Adds discount and activation support to the existing promotions table.
-- Run this migration once against the sandwich_maker_api MySQL database.

USE sandwich_maker_api;

ALTER TABLE promotions
    ADD COLUMN discount_percent DECIMAL(5,2) NOT NULL,
    ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;
