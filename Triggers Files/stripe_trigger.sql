DELIMITER //

CREATE TRIGGER stripe_to_main_payment_trigger_insert
AFTER INSERT ON payment_stripe_payment
FOR EACH ROW
BEGIN
    DECLARE user_id integer;
    DECLARE product_id integer;
    SELECT id INTO user_id FROM user_main_user WHERE BINARY email = NEW.customer_email LIMIT 1;
    SELECT id INTO product_id FROM products_main_product WHERE BINARY product_name = BINARY NEW.product_name LIMIT 1;

    INSERT INTO payment_main_payment(
        source_payment_id,
        candidate_name,
        candidate_phone,
        product_id,
        amount,
        order_datetime,
        status,
        currency,
        source,
        description,
        user_id,
        alnafi_payment_id
    ) VALUES (
        NEW.payment_id,
        NEW.name,
        NEW.phone,
        product_id,
        NEW.amount,
        NEW.order_datetime,
        NEW.status,
        NEW.currency,
        'Stripe',
        NEW.description,
        user_id,
        NEW.alnafi_order_id
    );
END//

DELIMITER ;

------------------------------------------------------

DELIMITER //
CREATE TRIGGER stripe_to_main_payment_trigger_update
AFTER UPDATE ON payment_stripe_payment
FOR EACH ROW
BEGIN
    DECLARE user_id integer;
    DECLARE product_id integer;
    SELECT id INTO user_id FROM user_main_user WHERE BINARY email = NEW.customer_email LIMIT 1;
    SELECT id INTO product_id FROM products_main_product WHERE BINARY product_name = BINARY NEW.product_name LIMIT 1;

    UPDATE payment_main_payment SET
        source_payment_id = NEW.payment_id,
        candidate_name = NEW.name,
        candidate_phone = NEW.phone,
        product_id = product_id,
        amount = NEW.amount,
        order_datetime = NEW.order_datetime,
        status = NEW.status,
        currency = NEW.currency,
        source = 'Stripe',
        description = NEW.description,
        user_id = user_id,
        alnafi_payment_id = NEW.alnafi_order_id
    WHERE source_payment_id = NEW.payment_id AND source = 'Stripe';
END//
DELIMITER ;

-----------------------------------------------

DELIMITER //

CREATE TRIGGER stripe_to_main_payment_trigger_delete
AFTER DELETE ON payment_stripe_payment
FOR EACH ROW
BEGIN
    DELETE FROM payment_main_payment
    WHERE source_payment_id = OLD.payment_id AND source = 'Stripe';
END//

DELIMITER ;
