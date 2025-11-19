-- Script para asegurar que admin2@camaravalencia.es tenga acceso completo de administrador
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. Buscar el usuario por email en auth.users y actualizar su perfil
UPDATE public.profiles p
SET 
  role = 'admin',
  active = true,
  first_name = COALESCE(p.first_name, 'Carlos'),
  last_name = COALESCE(p.last_name, 'López'),
  updated_at = now()
WHERE p.user_id IN (
  SELECT id 
  FROM auth.users 
  WHERE email = 'admin2@camaravalencia.es'
);

-- 2. Si el perfil no existe, crearlo (esto debería manejarse automáticamente por el trigger, pero por si acaso)
INSERT INTO public.profiles (user_id, email, first_name, last_name, role, active)
SELECT 
  id,
  email,
  'Carlos',
  'López',
  'admin',
  true
FROM auth.users
WHERE email = 'admin2@camaravalencia.es'
AND id NOT IN (SELECT user_id FROM public.profiles)
ON CONFLICT (user_id) DO UPDATE
SET 
  role = 'admin',
  active = true,
  first_name = COALESCE(profiles.first_name, 'Carlos'),
  last_name = COALESCE(profiles.last_name, 'López'),
  email = EXCLUDED.email,
  updated_at = now();

-- 3. Verificar que el usuario tiene acceso completo
-- Verificar políticas RLS para admins en todas las tablas principales

-- Asegurar que los usuarios pueden ver su propio perfil (política base)
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;
CREATE POLICY "Users can view their own profile" 
ON public.profiles
FOR SELECT 
USING (auth.uid() = user_id);

-- Asegurar que los admins pueden ver todos los perfiles (incluido el suyo)
DROP POLICY IF EXISTS "Admins can view all profiles" ON public.profiles;
CREATE POLICY "Admins can view all profiles" 
ON public.profiles
FOR SELECT 
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Asegurar que los admins pueden actualizar todos los perfiles
DROP POLICY IF EXISTS "Admins can update all profiles" ON public.profiles;
CREATE POLICY "Admins can update all profiles"
ON public.profiles
FOR UPDATE
USING (
  auth.uid() = user_id
  OR EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Asegurar que los admins pueden ver TODAS las encuestas (activas e inactivas)
DROP POLICY IF EXISTS "Anyone can view active surveys" ON public.surveys;
DROP POLICY IF EXISTS "Admins can view all surveys" ON public.surveys;
CREATE POLICY "Admins can view all surveys"
ON public.surveys
FOR SELECT
USING (
  active = true 
  OR auth.uid() = created_by
  OR EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Política para usuarios normales (solo encuestas activas)
CREATE POLICY "Anyone can view active surveys"
ON public.surveys
FOR SELECT
USING (active = true);

-- Asegurar que los admins pueden ver todas las respuestas
-- (Esta política ya debería existir, pero la verificamos)
DROP POLICY IF EXISTS "Admins can view all responses" ON public.survey_responses;
CREATE POLICY "Admins can view all responses"
ON public.survey_responses
FOR SELECT
USING (
  auth.uid() = user_id
  OR EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Verificar el resultado
SELECT 
  p.email,
  p.first_name,
  p.last_name,
  p.role,
  p.active,
  p.created_at
FROM public.profiles p
INNER JOIN auth.users au ON p.user_id = au.id
WHERE au.email = 'admin2@camaravalencia.es';

