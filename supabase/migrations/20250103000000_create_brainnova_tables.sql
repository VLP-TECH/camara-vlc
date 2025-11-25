-- Migración para crear las tablas del sistema Brainnova
-- Adaptado de schema.sql del backend

-- Tabla de dimensiones
CREATE TABLE IF NOT EXISTS public.dimensiones (
    nombre VARCHAR(40) PRIMARY KEY,
    peso INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla de subdimensiones
CREATE TABLE IF NOT EXISTS public.subdimensiones (
    nombre VARCHAR(100) PRIMARY KEY,
    nombre_dimension VARCHAR(40) NOT NULL REFERENCES public.dimensiones(nombre) ON DELETE CASCADE,
    peso INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla de definición de indicadores
CREATE TABLE IF NOT EXISTS public.definicion_indicadores (
    nombre VARCHAR(100) PRIMARY KEY,
    nombre_subdimension VARCHAR(100) NOT NULL REFERENCES public.subdimensiones(nombre) ON DELETE CASCADE,
    importancia VARCHAR(30),
    formula VARCHAR(50),
    fuente VARCHAR(50),
    origen_indicador VARCHAR(30),
    año_inicio INTEGER, -- Campo añadido según el TODO
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla de componentes de indicador
CREATE TABLE IF NOT EXISTS public.componentes_indicador (
    id SERIAL PRIMARY KEY,
    nombre_indicador VARCHAR(100) NOT NULL REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
    descripcion_dato VARCHAR(100),
    fuente_tabla VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla de resultados de indicadores
CREATE TABLE IF NOT EXISTS public.resultado_indicadores (
    id SERIAL PRIMARY KEY,
    nombre_indicador VARCHAR(100) NOT NULL REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
    valor_calculado DECIMAL(10,2),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER NOT NULL,
    sector VARCHAR(100),
    tamano_empresa VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    UNIQUE(nombre_indicador, pais, provincia, periodo, sector, tamano_empresa)
);

-- Tabla de datos crudos
CREATE TABLE IF NOT EXISTS public.datos_crudos (
    id SERIAL PRIMARY KEY,
    nombre_indicador VARCHAR(100) REFERENCES public.definicion_indicadores(nombre) ON DELETE CASCADE,
    valor DECIMAL(15,4),
    unidad VARCHAR(30),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER NOT NULL,
    descripcion_dato VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Tabla de datos macro
CREATE TABLE IF NOT EXISTS public.datos_macro (
    id SERIAL PRIMARY KEY,
    valor DECIMAL(15,4),
    unidad VARCHAR(30),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER NOT NULL,
    descripcion_dato VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_nombre ON public.resultado_indicadores(nombre_indicador);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_pais ON public.resultado_indicadores(pais);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_periodo ON public.resultado_indicadores(periodo);
CREATE INDEX IF NOT EXISTS idx_resultado_indicadores_pais_periodo ON public.resultado_indicadores(pais, periodo);
CREATE INDEX IF NOT EXISTS idx_datos_crudos_nombre ON public.datos_crudos(nombre_indicador);
CREATE INDEX IF NOT EXISTS idx_datos_crudos_periodo ON public.datos_crudos(periodo);
CREATE INDEX IF NOT EXISTS idx_datos_macro_periodo ON public.datos_macro(periodo);

-- Habilitar RLS
ALTER TABLE public.dimensiones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subdimensiones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.definicion_indicadores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.componentes_indicador ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.resultado_indicadores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.datos_crudos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.datos_macro ENABLE ROW LEVEL SECURITY;

-- Políticas RLS: Lectura pública, escritura solo para admins
CREATE POLICY "Anyone can view dimensiones"
ON public.dimensiones FOR SELECT
USING (true);

CREATE POLICY "Admins can manage dimensiones"
ON public.dimensiones FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view subdimensiones"
ON public.subdimensiones FOR SELECT
USING (true);

CREATE POLICY "Admins can manage subdimensiones"
ON public.subdimensiones FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view definicion_indicadores"
ON public.definicion_indicadores FOR SELECT
USING (true);

CREATE POLICY "Admins can manage definicion_indicadores"
ON public.definicion_indicadores FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view componentes_indicador"
ON public.componentes_indicador FOR SELECT
USING (true);

CREATE POLICY "Admins can manage componentes_indicador"
ON public.componentes_indicador FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view resultado_indicadores"
ON public.resultado_indicadores FOR SELECT
USING (true);

CREATE POLICY "Admins can manage resultado_indicadores"
ON public.resultado_indicadores FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view datos_crudos"
ON public.datos_crudos FOR SELECT
USING (true);

CREATE POLICY "Admins can manage datos_crudos"
ON public.datos_crudos FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

CREATE POLICY "Anyone can view datos_macro"
ON public.datos_macro FOR SELECT
USING (true);

CREATE POLICY "Admins can manage datos_macro"
ON public.datos_macro FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Triggers para updated_at
CREATE TRIGGER update_dimensiones_updated_at
BEFORE UPDATE ON public.dimensiones
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_subdimensiones_updated_at
BEFORE UPDATE ON public.subdimensiones
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_definicion_indicadores_updated_at
BEFORE UPDATE ON public.definicion_indicadores
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_resultado_indicadores_updated_at
BEFORE UPDATE ON public.resultado_indicadores
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

