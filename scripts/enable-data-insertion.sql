-- Script para habilitar inserción de datos en Supabase
-- Ejecuta este script en el SQL Editor de Supabase:
-- https://supabase.com/dashboard/project/aoykpiievtadhwssugvs/sql/new
-- 
-- ⚠️  IMPORTANTE: Después de cargar los datos, considera eliminar estas políticas
--     para mayor seguridad, dejando solo las políticas de admin

-- Dimensiones
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.dimensiones;
CREATE POLICY "Allow insert for data loading"
ON public.dimensiones FOR INSERT
WITH CHECK (true);

-- Subdimensiones
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.subdimensiones;
CREATE POLICY "Allow insert for data loading"
ON public.subdimensiones FOR INSERT
WITH CHECK (true);

-- Definición de indicadores
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.definicion_indicadores;
CREATE POLICY "Allow insert for data loading"
ON public.definicion_indicadores FOR INSERT
WITH CHECK (true);

-- Componentes de indicador
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.componentes_indicador;
CREATE POLICY "Allow insert for data loading"
ON public.componentes_indicador FOR INSERT
WITH CHECK (true);

-- Resultado de indicadores
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.resultado_indicadores;
CREATE POLICY "Allow insert for data loading"
ON public.resultado_indicadores FOR INSERT
WITH CHECK (true);

-- Datos crudos
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.datos_crudos;
CREATE POLICY "Allow insert for data loading"
ON public.datos_crudos FOR INSERT
WITH CHECK (true);

-- Datos macro
DROP POLICY IF EXISTS "Allow insert for data loading" ON public.datos_macro;
CREATE POLICY "Allow insert for data loading"
ON public.datos_macro FOR INSERT
WITH CHECK (true);

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE '✅ Políticas de inserción habilitadas. Ahora puedes ejecutar el script de carga de datos.';
END $$;

