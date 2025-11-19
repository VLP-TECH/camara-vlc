-- Script para corregir la recursión infinita en las políticas RLS
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. Crear función helper para verificar si un usuario es admin (evita recursión)
CREATE OR REPLACE FUNCTION public.is_admin(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = user_uuid
    AND role = 'admin'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- 2. Eliminar políticas problemáticas de profiles
DROP POLICY IF EXISTS "Admins can view all profiles" ON public.profiles;
DROP POLICY IF EXISTS "Users can view their own profile" ON public.profiles;

-- 3. Crear políticas corregidas usando la función helper
-- Política para que usuarios vean su propio perfil
CREATE POLICY "Users can view their own profile" 
ON public.profiles
FOR SELECT 
USING (auth.uid() = user_id);

-- Política para que admins vean todos los perfiles (usando función para evitar recursión)
CREATE POLICY "Admins can view all profiles" 
ON public.profiles
FOR SELECT 
USING (public.is_admin(auth.uid()));

-- 4. Corregir políticas de actualización
DROP POLICY IF EXISTS "Admins can update all profiles" ON public.profiles;
CREATE POLICY "Admins can update all profiles"
ON public.profiles
FOR UPDATE
USING (
  auth.uid() = user_id
  OR public.is_admin(auth.uid())
);

-- 5. Corregir políticas de surveys usando la función helper
DROP POLICY IF EXISTS "Admins can view all surveys" ON public.surveys;
DROP POLICY IF EXISTS "Anyone can view active surveys" ON public.surveys;

CREATE POLICY "Admins can view all surveys"
ON public.surveys
FOR SELECT
USING (
  active = true 
  OR auth.uid() = created_by
  OR public.is_admin(auth.uid())
);

CREATE POLICY "Anyone can view active surveys"
ON public.surveys
FOR SELECT
USING (active = true);

-- 6. Corregir políticas de survey_questions
DROP POLICY IF EXISTS "Admins can view all questions" ON public.survey_questions;
DROP POLICY IF EXISTS "Anyone can view questions of active surveys" ON public.survey_questions;

CREATE POLICY "Anyone can view questions of active surveys"
ON public.survey_questions
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.surveys
    WHERE surveys.id = survey_questions.survey_id
    AND (
      surveys.active = true 
      OR surveys.created_by = auth.uid()
      OR public.is_admin(auth.uid())
    )
  )
);

-- 7. Corregir políticas de survey_responses
DROP POLICY IF EXISTS "Admins can view all responses" ON public.survey_responses;
CREATE POLICY "Admins can view all responses"
ON public.survey_responses
FOR SELECT
USING (
  auth.uid() = user_id
  OR public.is_admin(auth.uid())
);

-- 8. Corregir políticas de creación y actualización de surveys
DROP POLICY IF EXISTS "Admins and editors can create surveys" ON public.surveys;
DROP POLICY IF EXISTS "Admins and editors can update surveys" ON public.surveys;

CREATE POLICY "Admins and editors can create surveys"
ON public.surveys
FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND (role = 'admin' OR role = 'editor')
  )
);

CREATE POLICY "Admins and editors can update surveys"
ON public.surveys
FOR UPDATE
USING (
  auth.uid() = created_by
  OR EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND (role = 'admin' OR role = 'editor')
  )
);

-- 9. Verificar que no hay recursión
SELECT 'Políticas corregidas. Verificando...' as status;

