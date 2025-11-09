-- Confirmar email del usuario demo@camaravalencia.es
UPDATE auth.users 
SET email_confirmed_at = now()
WHERE email = 'demo@camaravalencia.es';