-- ============================================================
-- ChauchaApp QA Seed Data
-- ============================================================
-- Test users for authentication testing (login & register flows).
-- All passwords are hashed with bcrypt via pgcrypto extension.
--
-- Default test password for ALL users: TestPass123!
-- ============================================================

-- Ensure pgcrypto is available for password hashing
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- TEST USERS
-- ============================================================
-- 10 test users with varied income types and financial profiles.
-- 2 specific users for login/register test cases:
--   - test_login@chauchaapp.cl  (for login tests)
--   - test_register@chauchaapp.cl (for register flow tests)
-- ============================================================

INSERT INTO "user" (
    first_name, last_name, email, password,
    birth_date, income_type_id, monthly_income, monthly_expenses
) VALUES
    -- User 1: Login test user
    (
        'Test', 'Login',
        'test_login@chauchaapp.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1990-05-15',
        (SELECT income_type_id FROM income_type WHERE name = 'Sueldo fijo'),
        850000.00, 620000.00
    ),
    -- User 2: Register flow test user
    (
        'Test', 'Register',
        'test_register@chauchaapp.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1995-08-22',
        (SELECT income_type_id FROM income_type WHERE name = 'Independiente'),
        1200000.00, 780000.00
    ),
    -- User 3: María González - Salaried
    (
        'María', 'González',
        'maria.gonzalez@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1988-03-10',
        (SELECT income_type_id FROM income_type WHERE name = 'Sueldo fijo'),
        1500000.00, 980000.00
    ),
    -- User 4: Carlos Muñoz - Independent
    (
        'Carlos', 'Muñoz',
        'carlos.munoz@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1992-11-28',
        (SELECT income_type_id FROM income_type WHERE name = 'Independiente'),
        2000000.00, 1350000.00
    ),
    -- User 5: Valentina Rojas - Mixed
    (
        'Valentina', 'Rojas',
        'valentina.rojas@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1985-07-03',
        (SELECT income_type_id FROM income_type WHERE name = 'Mixto'),
        1800000.00, 1100000.00
    ),
    -- User 6: Andrés Silva - Salaried
    (
        'Andrés', 'Silva',
        'andres.silva@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1998-01-20',
        (SELECT income_type_id FROM income_type WHERE name = 'Sueldo fijo'),
        650000.00, 520000.00
    ),
    -- User 7: Camila Torres - Other
    (
        'Camila', 'Torres',
        'camila.torres@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1993-09-14',
        (SELECT income_type_id FROM income_type WHERE name = 'Otro'),
        900000.00, 670000.00
    ),
    -- User 8: Diego Fernández - Salaried
    (
        'Diego', 'Fernández',
        'diego.fernandez@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1987-12-05',
        (SELECT income_type_id FROM income_type WHERE name = 'Sueldo fijo'),
        2500000.00, 1800000.00
    ),
    -- User 9: Javiera López - Independent
    (
        'Javiera', 'López',
        'javiera.lopez@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1996-04-18',
        (SELECT income_type_id FROM income_type WHERE name = 'Independiente'),
        1100000.00, 850000.00
    ),
    -- User 10: Felipe Martínez - Mixed
    (
        'Felipe', 'Martínez',
        'felipe.martinez@test.cl',
        crypt('TestPass123!', gen_salt('bf')),
        '1991-06-30',
        (SELECT income_type_id FROM income_type WHERE name = 'Mixto'),
        3000000.00, 2100000.00
    )
ON CONFLICT (email) DO NOTHING;

-- ============================================================
-- SAMPLE TRANSACTIONS
-- ============================================================
-- Transactions for test_login@chauchaapp.cl
-- ============================================================

INSERT INTO "transaction" (
    user_id, transaction_type_id, transaction_category_id, 
    transaction_frequency_id, amount, description, transaction_date
)
SELECT 
    u.user_id, 
    (SELECT transaction_type_id FROM transaction_type WHERE name = 'Ingreso'),
    (SELECT transaction_category_id FROM transaction_category WHERE name = 'Sueldo'),
    (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'),
    850000.00, 'Sueldo Abril', '2026-04-01'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl'
ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (
    user_id, transaction_type_id, transaction_category_id, 
    transaction_frequency_id, amount, description, transaction_date
)
SELECT 
    u.user_id, 
    (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'),
    (SELECT transaction_category_id FROM transaction_category WHERE name = 'Alimentación'),
    (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'),
    45000.00, 'Súper Líder', '2026-04-05'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl'
ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (
    user_id, transaction_type_id, transaction_category_id, 
    transaction_frequency_id, amount, description, transaction_date
)
SELECT 
    u.user_id, 
    (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'),
    (SELECT transaction_category_id FROM transaction_category WHERE name = 'Transporte'),
    (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'),
    15000.00, 'Carga Bip', '2026-04-06'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl'
ON CONFLICT DO NOTHING;

-- More transactions for previous months (March)
INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Ingreso'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Sueldo'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 850000.00, 'Sueldo Marzo', '2026-03-01'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Vivienda'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 350000.00, 'Arriendo Marzo', '2026-03-05'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

-- More transactions for previous months (February)
INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Ingreso'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Sueldo'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 850000.00, 'Sueldo Febrero', '2026-02-01'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Salud'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 85000.00, 'Dentista', '2026-02-15'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

-- NEW DATA FOR QA (MAY & HEAVY APRIL)
-- Current Month: May 2026
INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Ingreso'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Sueldo'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 850000.00, 'Sueldo Mayo', '2026-05-01'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Vivienda'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 350000.00, 'Arriendo Mayo', '2026-05-05'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Alimentación'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 55000.00, 'Supermercado Mayo', '2026-05-03'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Transporte'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 15000.00, 'Carga Bip Mayo', '2026-05-07'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Servicios Básicos'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 42000.00, 'Luz y Agua Mayo', '2026-05-10'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

-- Heavy Expenses Month: April 2026
INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Vivienda'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Mensual'), 350000.00, 'Arriendo Abril', '2026-04-05'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Salud'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 150000.00, 'Consulta Médica Especialista', '2026-04-08'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Educación'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 200000.00, 'Curso Desarrollo Web', '2026-04-12'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Entretenimiento'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 95000.00, 'Cena Aniversario', '2026-04-18'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Otros Gastos'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 60000.00, 'Compra Imprevista', '2026-04-22'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;

INSERT INTO "transaction" (user_id, transaction_type_id, transaction_category_id, transaction_frequency_id, amount, description, transaction_date)
SELECT u.user_id, (SELECT transaction_type_id FROM transaction_type WHERE name = 'Gasto'), (SELECT transaction_category_id FROM transaction_category WHERE name = 'Alimentación'), (SELECT transaction_frequency_id FROM transaction_frequency WHERE name = 'Única'), 70000.00, 'Supermercado Extra Abril', '2026-04-25'
FROM "user" u WHERE u.email = 'test_login@chauchaapp.cl' ON CONFLICT DO NOTHING;


-- ============================================================
-- QA SEED COMPLETE
-- ============================================================
-- Test credentials summary:
--
-- | Email                          | Password      | Income Type  |
-- |--------------------------------|---------------|-------------|
-- | test_login@chauchaapp.cl       | TestPass123!  | salaried    |
-- | test_register@chauchaapp.cl    | TestPass123!  | independent |
-- | maria.gonzalez@test.cl         | TestPass123!  | salaried    |
-- | carlos.munoz@test.cl           | TestPass123!  | independent |
-- | valentina.rojas@test.cl        | TestPass123!  | mixed       |
-- | andres.silva@test.cl           | TestPass123!  | salaried    |
-- | camila.torres@test.cl          | TestPass123!  | other       |
-- | diego.fernandez@test.cl        | TestPass123!  | salaried    |
-- | javiera.lopez@test.cl          | TestPass123!  | independent |
-- | felipe.martinez@test.cl        | TestPass123!  | mixed       |
-- ============================================================
