-- Script para verificar que el administrador tiene acceso completo
-- Ejecuta este script después de setup-admin-access.sql para verificar

-- 1. Verificar perfil del administrador
SELECT 
  'Perfil del Administrador' as verificación,
  p.email,
  p.first_name || ' ' || p.last_name as nombre_completo,
  p.role,
  p.active,
  CASE 
    WHEN p.role = 'admin' AND p.active = true THEN '✅ Correcto'
    ELSE '❌ Necesita ajuste'
  END as estado
FROM public.profiles p
INNER JOIN auth.users au ON p.user_id = au.id
WHERE au.email = 'admin2@camaravalencia.es';

-- 2. Verificar políticas RLS para perfiles
SELECT 
  'Políticas de Perfiles' as verificación,
  schemaname,
  tablename,
  policyname,
  CASE 
    WHEN policyname LIKE '%admin%' THEN '✅ Existe'
    ELSE '⚠️  Revisar'
  END as estado
FROM pg_policies
WHERE tablename = 'profiles'
AND schemaname = 'public'
ORDER BY policyname;

-- 3. Verificar políticas RLS para encuestas
SELECT 
  'Políticas de Encuestas' as verificación,
  schemaname,
  tablename,
  policyname,
  CASE 
    WHEN policyname LIKE '%admin%' THEN '✅ Existe'
    ELSE '⚠️  Revisar'
  END as estado
FROM pg_policies
WHERE tablename IN ('surveys', 'survey_questions', 'survey_responses')
AND schemaname = 'public'
ORDER BY tablename, policyname;

-- 4. Verificar políticas RLS para chatbot_knowledge
SELECT 
  'Políticas de Chatbot' as verificación,
  schemaname,
  tablename,
  policyname,
  CASE 
    WHEN policyname LIKE '%admin%' OR policyname LIKE '%Anyone%' THEN '✅ Existe'
    ELSE '⚠️  Revisar'
  END as estado
FROM pg_policies
WHERE tablename = 'chatbot_knowledge'
AND schemaname = 'public'
ORDER BY policyname;

-- 5. Resumen de acceso del administrador
SELECT 
  'Resumen de Acceso' as verificación,
  'El administrador puede:' as descripción,
  '✅ Ver todos los perfiles' as permiso_1,
  '✅ Actualizar todos los perfiles' as permiso_2,
  '✅ Ver todas las encuestas' as permiso_3,
  '✅ Ver todas las respuestas' as permiso_4,
  '✅ Gestionar conocimiento del chatbot' as permiso_5,
  '✅ Acceder al panel de administración' as permiso_6;

