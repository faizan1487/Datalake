DELIMITER //

CREATE TRIGGER ubl_manual_to_main_payment_trigger_insert
AFTER INSERT ON payment_ubl_manual_payment
FOR EACH ROW
BEGIN
    DECLARE user_id integer;
    DECLARE product_id integer;
    SELECT id INTO user_id FROM user_main_user WHERE email = NEW.customer_email;
    SELECT id INTO product_id FROM products_main_product WHERE product_name = NEW.product_name;

    INSERT INTO payment_main_payment(
        candidate_name,
        depositor_name,
        user_id,
        amount,
        product_id,
        status,
        internal_source,
        source_payment_id,
        source,
        candidate_phone,
        created_datetime,
        order_datetime,
        payment_proof

    ) VALUES (
        NEW.candidate_name,
        NEW.depositor_name,
        user_id,
        NEW.amount,
        product_id,
        NEW.status,
        NEW.payment_channel,
        NEW.transaction_id,
        'UBL_Manual',
        NEW.candidate_phone,
        NEW.created_at,
        NEW.deposit_date,
        NEW.transaction_image
    );
END//

DELIMITER ;

------------------------------------

DELIMITER //
CREATE TRIGGER ubl_manual_to_main_payment_trigger_update
AFTER UPDATE ON payment_ubl_manual_payment
FOR EACH ROW
BEGIN
    DECLARE user_id integer;
    DECLARE product_id integer;
    SELECT id INTO user_id FROM user_main_user WHERE BINARY email = NEW.customer_email LIMIT 1;
    SELECT id INTO product_id FROM products_main_product WHERE BINARY product_name = BINARY NEW.product_name LIMIT 1;

    UPDATE payment_main_payment SET
        candidate_name = NEW.candidate_name,
        depositor_name = NEW.depositor_name,
        user_id = user_id,
        amount = NEW.amount,
        product_id = product_id,
        status = NEW.status,
        internal_source = NEW.payment_channel,
        source_payment_id = NEW.transaction_id,
        source = 'UBL_Manual',
        candidate_phone = NEW.candidate_phone,
        created_datetime = NEW.created_at,
        order_datetime = NEW.deposit_date,
        payment_proof = NEW.transaction_image
    WHERE source_payment_id = NEW.transaction_id AND source = 'UBL_Manual';
END//
DELIMITER ;

-----------------------------------------------

DELIMITER //

CREATE TRIGGER ubl_manual_to_main_payment_trigger_delete
AFTER DELETE ON payment_ubl_manual_payment
FOR EACH ROW
BEGIN
    DELETE FROM payment_main_payment
    WHERE source_payment_id = NEW.transaction_id AND source = 'UBL_Manual';
END//

DELIMITER ;















source_payment_id
alnafi_payment_id
card_mask
amount
currency
source
internal_source
status
order_datetime
expiration_datetime
activation_datetime
token_paid_datetime
created_datetime
ubl_captured
ubl_reversed
ubl_refund
ubl_approval_code
description
payment_proof
send_invoice
pk_invoice_number
us_invoice_number
sponsored
coupon_code
is_upgrade_payment
affiliate
ubl_depositor_name
ubl_payment_channel
bin_bank_name
product_id
user_id