-- Migración para permitir inserción de datos durante la carga inicial
-- Esta migración añade políticas temporales que permiten inserción pública
-- ⚠️  IMPORTANTE: Después de cargar los datos, considera eliminar estas políticas
--     para mayor seguridad, dejando solo las políticas de admin

-- Políticas para permitir inserción durante carga inicial
-- Estas políticas permiten que cualquier usuario (incluso anónimo) pueda insertar datos
-- Útil para scripts de carga inicial de datos

-- Dimensiones
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'dimensiones' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.dimensiones FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Subdimensiones
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'subdimensiones' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.subdimensiones FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Definición de indicadores
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'definicion_indicadores' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.definicion_indicadores FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Componentes de indicador
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'componentes_indicador' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.componentes_indicador FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Resultado de indicadores
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'resultado_indicadores' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.resultado_indicadores FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Datos crudos
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_crudos' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.datos_crudos FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

-- Datos macro
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_macro' 
        AND policyname = 'Allow insert for data loading'
    ) THEN
        CREATE POLICY "Allow insert for data loading"
        ON public.datos_macro FOR INSERT
        WITH CHECK (true);
    END IF;
END $$;

