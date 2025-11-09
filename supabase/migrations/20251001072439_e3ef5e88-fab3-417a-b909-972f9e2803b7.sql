-- Insert example survey
INSERT INTO public.surveys (title, description, created_by, active)
VALUES (
  'Encuesta del Ecosistema Digital Valenciano 2025',
  'Ayúdanos a conocer mejor el panorama digital de la Comunidad Valenciana. Esta encuesta nos permitirá identificar tendencias, necesidades y oportunidades de mejora en nuestro ecosistema.',
  (SELECT user_id FROM public.profiles WHERE role = 'admin' LIMIT 1),
  true
);

-- Insert example questions for the survey
INSERT INTO public.survey_questions (survey_id, question_text, question_type, options, order_index, required)
VALUES 
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    '¿Cuál es el nombre de tu empresa u organización?',
    'text',
    NULL,
    1,
    true
  ),
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    '¿En qué sector opera principalmente tu organización?',
    'multiple_choice',
    '{"options": ["Tecnología y Software", "Servicios Digitales", "E-commerce", "Consultoría TIC", "Educación y Formación", "Salud Digital", "Fintech", "Otro"]}'::jsonb,
    2,
    true
  ),
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    '¿Cuántos empleados tiene tu organización?',
    'multiple_choice',
    '{"options": ["1-10", "11-50", "51-200", "201-500", "Más de 500"]}'::jsonb,
    3,
    true
  ),
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    '¿Cuáles son los principales retos que enfrenta tu organización en el ámbito digital?',
    'textarea',
    NULL,
    4,
    true
  ),
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    '¿Qué tipo de apoyo necesitarías del ecosistema digital valenciano?',
    'multiple_choice',
    '{"options": ["Financiación", "Formación y capacitación", "Networking y colaboraciones", "Infraestructura tecnológica", "Asesoramiento legal y fiscal", "Acceso a talento", "Todos los anteriores"]}'::jsonb,
    5,
    true
  ),
  (
    (SELECT id FROM public.surveys WHERE title = 'Encuesta del Ecosistema Digital Valenciano 2025' LIMIT 1),
    'Comentarios adicionales o sugerencias',
    'textarea',
    NULL,
    6,
    false
  );