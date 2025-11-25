-- Migración para crear las tablas del sistema Brainnova
-- Esquema exacto según especificación del backend
-- Adaptado de MySQL a PostgreSQL

-- Verificar y crear tabla de dimensiones
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'dimensiones') THEN
        CREATE TABLE public.dimensiones (
            nombre VARCHAR(40) PRIMARY KEY,
            peso INTEGER NOT NULL
        );
    END IF;
END $$;

-- Verificar y crear tabla de subdimensiones
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'subdimensiones') THEN
        CREATE TABLE public.subdimensiones (
            nombre VARCHAR(100) PRIMARY KEY,
            nombre_dimension VARCHAR(40) NOT NULL REFERENCES public.dimensiones(nombre) ON DELETE CASCADE,
            peso INTEGER NOT NULL
        );
    END IF;
END $$;

-- Verificar y crear tabla de definición de indicadores
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'definicion_indicadores') THEN
        CREATE TABLE public.definicion_indicadores (
            nombre VARCHAR(100) PRIMARY KEY,
            nombre_subdimension VARCHAR(100) NOT NULL REFERENCES public.subdimensiones(nombre) ON DELETE CASCADE,
            importancia VARCHAR(30),
            formula VARCHAR(50),
            fuente VARCHAR(50),
            origen_indicador VARCHAR(30)
        );
    END IF;
END $$;

-- Verificar y crear tabla de componentes de indicador
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'componentes_indicador') THEN
        CREATE TABLE public.componentes_indicador (
            id SERIAL PRIMARY KEY,
            nombre_indicador VARCHAR(100) NOT NULL REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
            descripcion_dato VARCHAR(100),
            fuente_tabla VARCHAR(100)
        );
    END IF;
END $$;

-- Verificar y crear tabla de resultados de indicadores
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'resultado_indicadores') THEN
        CREATE TABLE public.resultado_indicadores (
            id SERIAL PRIMARY KEY,
            nombre_indicador VARCHAR(100) NOT NULL REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
            valor_calculado DECIMAL(5,2),
            pais VARCHAR(30),
            provincia VARCHAR(30),
            periodo INTEGER NOT NULL
        );
    END IF;
END $$;

-- Verificar y crear tabla de datos crudos
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_crudos') THEN
        CREATE TABLE public.datos_crudos (
            id SERIAL PRIMARY KEY,
            nombre_indicador VARCHAR(100) REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
            valor DECIMAL,
            unidad VARCHAR(30),
            pais VARCHAR(30),
            provincia VARCHAR(30),
            periodo INTEGER NOT NULL,
            descripcion_dato VARCHAR(50)
        );
    END IF;
END $$;

-- Verificar y crear tabla de datos macro
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_macro') THEN
        CREATE TABLE public.datos_macro (
            id SERIAL PRIMARY KEY,
            valor DECIMAL,
            unidad VARCHAR(30),
            pais VARCHAR(30),
            provincia VARCHAR(30),
            periodo INTEGER NOT NULL,
            descripcion_dato VARCHAR(50)
        );
    END IF;
END $$;

-- Crear índices para mejorar el rendimiento (si no existen)
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_nombre ON public.resultado_indicadores(nombre_indicador);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_pais ON public.resultado_indicadores(pais);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_periodo ON public.resultado_indicadores(periodo);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_pais_periodo ON public.resultado_indicadores(pais, periodo);
CREATE INDEX IF NOT EXISTS idx_datos_crudos_nombre ON public.datos_crudos(nombre_indicador);
CREATE INDEX IF NOT EXISTS idx_datos_crudos_periodo ON public.datos_crudos(periodo);
CREATE INDEX IF NOT EXISTS idx_datos_macro_periodo ON public.datos_macro(periodo);

-- Habilitar RLS si no está habilitado
DO $$ 
BEGIN
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'dimensiones') THEN
        ALTER TABLE public.dimensiones ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'subdimensiones') THEN
        ALTER TABLE public.subdimensiones ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'definicion_indicadores') THEN
        ALTER TABLE public.definicion_indicadores ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'componentes_indicador') THEN
        ALTER TABLE public.componentes_indicador ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'resultado_indicadores') THEN
        ALTER TABLE public.resultado_indicadores ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_crudos') THEN
        ALTER TABLE public.datos_crudos ENABLE ROW LEVEL SECURITY;
    END IF;
    IF EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'datos_macro') THEN
        ALTER TABLE public.datos_macro ENABLE ROW LEVEL SECURITY;
    END IF;
END $$;

-- Crear políticas RLS si no existen
DO $$ 
BEGIN
    -- Políticas para dimensiones
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'dimensiones' 
        AND policyname = 'Anyone can view dimensiones'
    ) THEN
        CREATE POLICY "Anyone can view dimensiones"
        ON public.dimensiones FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'dimensiones' 
        AND policyname = 'Admins can manage dimensiones'
    ) THEN
CREATE POLICY "Admins can manage dimensiones"
ON public.dimensiones FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.dimensiones FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para subdimensiones
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'subdimensiones' 
        AND policyname = 'Anyone can view subdimensiones'
    ) THEN
        CREATE POLICY "Anyone can view subdimensiones"
        ON public.subdimensiones FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'subdimensiones' 
        AND policyname = 'Admins can manage subdimensiones'
    ) THEN
CREATE POLICY "Admins can manage subdimensiones"
ON public.subdimensiones FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.subdimensiones FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para definicion_indicadores
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'definicion_indicadores' 
        AND policyname = 'Anyone can view definicion_indicadores'
    ) THEN
        CREATE POLICY "Anyone can view definicion_indicadores"
        ON public.definicion_indicadores FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'definicion_indicadores' 
        AND policyname = 'Admins can manage definicion_indicadores'
    ) THEN
CREATE POLICY "Admins can manage definicion_indicadores"
ON public.definicion_indicadores FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.definicion_indicadores FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para componentes_indicador
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'componentes_indicador' 
        AND policyname = 'Anyone can view componentes_indicador'
    ) THEN
        CREATE POLICY "Anyone can view componentes_indicador"
        ON public.componentes_indicador FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'componentes_indicador' 
        AND policyname = 'Admins can manage componentes_indicador'
    ) THEN
CREATE POLICY "Admins can manage componentes_indicador"
ON public.componentes_indicador FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.componentes_indicador FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para resultado_indicadores
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'resultado_indicadores' 
        AND policyname = 'Anyone can view resultado_indicadores'
    ) THEN
        CREATE POLICY "Anyone can view resultado_indicadores"
        ON public.resultado_indicadores FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'resultado_indicadores' 
        AND policyname = 'Admins can manage resultado_indicadores'
    ) THEN
CREATE POLICY "Admins can manage resultado_indicadores"
ON public.resultado_indicadores FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.resultado_indicadores FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para datos_crudos
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_crudos' 
        AND policyname = 'Anyone can view datos_crudos'
    ) THEN
        CREATE POLICY "Anyone can view datos_crudos"
        ON public.datos_crudos FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_crudos' 
        AND policyname = 'Admins can manage datos_crudos'
    ) THEN
CREATE POLICY "Admins can manage datos_crudos"
ON public.datos_crudos FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM public.profiles
        WHERE user_id = auth.uid()
        AND role = 'admin'
    )
);

-- Política temporal para permitir inserción durante carga inicial
CREATE POLICY "Allow insert for data loading"
ON public.datos_crudos FOR INSERT
WITH CHECK (true);
    END IF;

    -- Políticas para datos_macro
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_macro' 
        AND policyname = 'Anyone can view datos_macro'
    ) THEN
        CREATE POLICY "Anyone can view datos_macro"
        ON public.datos_macro FOR SELECT
        USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE schemaname = 'public' 
        AND tablename = 'datos_macro' 
        AND policyname = 'Admins can manage datos_macro'
    ) THEN
        CREATE POLICY "Admins can manage datos_macro"
        ON public.datos_macro FOR ALL
        USING (
            EXISTS (
                SELECT 1 FROM public.profiles
                WHERE user_id = auth.uid()
                AND role = 'admin'
            )
        );
    END IF;
END $$;

