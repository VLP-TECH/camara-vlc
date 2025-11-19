-- Script para asegurar que los admins tengan acceso completo a encuestas
-- Ejecuta este script en el SQL Editor de Supabase

-- 1. Asegurar que los admins pueden ver TODAS las encuestas (activas e inactivas)
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

-- 2. Asegurar que los admins pueden crear encuestas
DROP POLICY IF EXISTS "Admins and editors can create surveys" ON public.surveys;
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

-- 3. Asegurar que los admins pueden actualizar TODAS las encuestas
DROP POLICY IF EXISTS "Admins and editors can update surveys" ON public.surveys;
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

-- 4. Asegurar que los admins pueden eliminar encuestas
DROP POLICY IF EXISTS "Admins can delete surveys" ON public.surveys;
CREATE POLICY "Admins can delete surveys"
ON public.surveys
FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- 5. Asegurar que los admins pueden ver TODAS las preguntas
DROP POLICY IF EXISTS "Admins can view all questions" ON public.survey_questions;
CREATE POLICY "Admins can view all questions"
ON public.survey_questions
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM public.surveys
    WHERE surveys.id = survey_questions.survey_id
    AND (
      surveys.active = true 
      OR surveys.created_by = auth.uid()
      OR EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
      )
    )
  )
);

-- 6. Asegurar que los admins pueden gestionar TODAS las preguntas
DROP POLICY IF EXISTS "Admins and editors can manage questions" ON public.survey_questions;
CREATE POLICY "Admins and editors can manage questions"
ON public.survey_questions
FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND (role = 'admin' OR role = 'editor')
  )
);

-- 7. Verificar políticas actuales
SELECT 
  'Políticas de Surveys' as tabla,
  policyname,
  cmd as operación
FROM pg_policies
WHERE tablename = 'surveys'
AND schemaname = 'public'
ORDER BY policyname;

SELECT 
  'Políticas de Survey Questions' as tabla,
  policyname,
  cmd as operación
FROM pg_policies
WHERE tablename = 'survey_questions'
AND schemaname = 'public'
ORDER BY policyname;

