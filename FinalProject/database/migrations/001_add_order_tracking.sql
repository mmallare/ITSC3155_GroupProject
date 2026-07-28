-- Adds customer-facing tracking support to the existing orders table.
-- Run this migration once against the sandwich_maker_api MySQL database.

USE sandwich_maker_api;

ALTER TABLE orders
    ADD COLUMN tracking_number VARCHAR(36) NOT NULL UNIQUE (UUID()),
    ADD COLUMN status VARCHAR(50) NOT NULL DEFAULT 'received';

ALTER TABLE orders
ADD CONSTRAINT uq_orders_tracking_number UNIQUE (tracking_number);
