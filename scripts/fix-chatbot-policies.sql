-- Script para ajustar las políticas RLS y permitir la carga inicial de datos
-- Ejecuta este script en el SQL Editor de Supabase DESPUÉS de crear la tabla

-- Eliminar la política restrictiva de inserción
DROP POLICY IF EXISTS "Admins can manage chatbot knowledge" ON public.chatbot_knowledge;

-- Crear política que permite inserción sin autenticación (para carga inicial)
-- Luego puedes restringirla si lo deseas
CREATE POLICY "Allow insert for initial data load"
ON public.chatbot_knowledge
FOR INSERT
WITH CHECK (true);

-- Mantener la política de lectura pública
-- (Ya debería existir, pero la recreamos por si acaso)
DROP POLICY IF EXISTS "Anyone can view chatbot knowledge" ON public.chatbot_knowledge;
CREATE POLICY "Anyone can view chatbot knowledge"
ON public.chatbot_knowledge
FOR SELECT
USING (true);

-- Política para actualización y eliminación (solo admins)
CREATE POLICY "Admins can update and delete chatbot knowledge"
ON public.chatbot_knowledge
FOR UPDATE
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Admins can delete chatbot knowledge"
ON public.chatbot_knowledge
FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

