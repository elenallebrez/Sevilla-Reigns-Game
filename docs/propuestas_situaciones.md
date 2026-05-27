# Propuestas de situaciones

Situaciones nuevas inspiradas en actualidad reciente de Sevilla. Estan pensadas para copiarse a `data/eventos.json`; no incluyen `image` y evitan temas ya presentes en el JSON actual como Feria, Semana Santa, metro, toldos, futbol, tapas veganas, toros, playas o privatizacion de Plaza de Espana.

## Fuentes consultadas

- Ayuntamiento de Sevilla: Plan Habitat Sevilla de Emvisesa para intervenir en 2.071 viviendas publicas en alquiler durante 2026. https://www.sevilla.org/actualidad/noticias/2026/la-junta-general-de-emvisesa-aprueba-una-ampliacion-de-capital-de-tres-millones-de-euros-para-impulsar-el-plan-habitat-sevilla
- Ayuntamiento de Sevilla: PAI "Sevilla Nuevo Este", con corredor verde y actuaciones en Este-Alcosa-Torreblanca. https://www.sevilla.org/actualidad/noticias/2026/el-ayuntamiento-inicia-la-seleccion-de-operaciones-del-pai-sevilla-nuevo-este
- Ayuntamiento de Sevilla: presupuesto municipal 2026 y refuerzo de Lipasam. https://www.sevilla.org/actualidad/noticias/2026/el-pleno-aprueba-definitivamente-el-presupuesto-para-2026-el-mas-alto-de-la-historia-de-sevilla
- Ayuntamiento de Sevilla: nuevo modelo de limpieza de colegios publicos. https://www.sevilla.org/actualidad/noticias/2026/el-gobierno-de-sanz-cambiara-el-modelo-de-limpieza-de-los-colegios-publicos-que-contara-con-maquinaria-casi-400-trabajadores-y-una-modernizacion-integral-del-servicio
- Ayuntamiento de Sevilla: proyecto de Zonas de Bajas Emisiones en Cartuja Norte y Cartuja Sur. https://www.sevilla.org/servicios/movilidad/zbe/proyecto-completo_zbe_sevilla_borr_v8-2.pdf
- Sevilla Actualidad: sensores de contaminacion y nuevo sistema de multas de la ZBE de Cartuja. https://www.sevillaactualidad.com/sevilla/586418-la-zbe-de-la-cartuja-contara-con-sensores-de-contaminacion-asi-funcionara-el-sistema-de-multas/
- Puerto de Sevilla: doble escala de cruceros Scenic Eclipse y nueva gestion de la terminal desde 2026. https://www.puertodesevilla.com/comunicacion/actualidad/el-puerto-de-sevilla-recibe-por-primera-vez-la-doble-escala-de-los-cruceros-gemelos-scenic-eclipse
- Cadena SER: nueva terminal de cruceros y megayates en el Paseo de las Delicias. https://cadenaser.com/andalucia/2026/04/24/el-puerto-inaugura-su-terminal-de-cruceros-la-intencion-es-ampliar-la-temporada-y-no-quedarnos-en-el-otono-y-primavera-radio-sevilla/
- Europa Press: terminal de cruceros y megayates orientada a escalas de mayor valor anadido. https://www.europapress.es/andalucia/sevilla-00357/noticia-nueva-terminal-cruceros-megayates-sevilla-ya-opera-objetivo-atraer-escalas-mayor-valor-anadido-20260426120952.html
- Huffington Post: tension vecinal en Santa Cruz por sustitucion de comercio cotidiano por souvenirs y turismo. https://www.huffingtonpost.es/sociedad/marisol-vecina-barrio-santa-cruz-sevilla-ya-quedan-panaderias-tiendas-souvenirs-colas-desayunar-f202604.html
- Aena: balance de trafico 2025 del Aeropuerto de Sevilla. https://www.aena.es/doc/detalleprensa/260113-svq-estadisticas-2025.pdf
- Ayuntamiento de Sevilla: ampliacion de proteccion de entornos BIC en el Conjunto Historico. https://www.sevilla.org/actualidad/noticias/2026/el-ayuntamiento-llevara-a-pleno-la-ampliacion-de-la-proteccion-de-los-entornos-bic-a-la-totalidad-de-sectores-del-conjunto-historico
- Ayuntamiento de Sevilla: convocatoria Efeso Sevilla para formacion e insercion laboral. https://www.sevilla.org/actualidad/noticias/2026/el-ayuntamiento-amplia-hasta-el-29-de-mayo-el-plazo-de-inscripcion-de-la-cuarta-convocatoria-de-efeso-sevilla
- El Pais: debate sobre agua regenerada de Sevilla para agricultura del entorno del Guadalquivir. https://elpais.com/clima-y-medio-ambiente/2026-05-06/el-agua-que-sobra-en-la-ciudad-y-falta-en-el-campo-queda-un-dia-menos-para-la-proxima-sequia.html

## JSON propuesto

```json
[
  {
    "id": "plan_habitat_emvisesa",
    "title": "Pintura, ascensor y paciencia",
    "description": "Emvisesa pide fondos para arreglar miles de viviendas publicas: fachadas, accesibilidad y algun ascensor que aun suena como una saeta oxidada.",
    "options": [
      {
        "text": "Rehabilita los bloques ya.",
        "effects": { "people": 15, "money": -15, "tourism": -5 },
        "desbloquea": ["derrama_vecinal_emvisesa"]
      },
      {
        "text": "Primero otra auditoria.",
        "effects": { "people": -15, "money": 5 }
      }
    ]
  },
  {
    "id": "derrama_vecinal_emvisesa",
    "title": "La obra eterna",
    "description": "Las obras han empezado, pero los vecinos llevan tres semanas entrando por una pasarela que parece montada por una chirigota de arquitectos.",
    "requisitos": ["plan_habitat_emvisesa"],
    "options": [
      {
        "text": "Paga refuerzos y termina antes.",
        "effects": { "people": 10, "money": -10 }
      },
      {
        "text": "Que se acostumbren al andamio.",
        "effects": { "people": -20, "money": 5 }
      }
    ]
  },
  {
    "id": "corredor_verde_este",
    "title": "Selva en Sevilla Este",
    "description": "El distrito Este-Alcosa-Torreblanca quiere un gran corredor verde que conecte barrios, sombra y paseos sin cruzar media ciudad en modo desierto.",
    "options": [
      {
        "text": "Planta arboles como si no hubiera agosto.",
        "effects": { "people": 15, "money": -10, "tourism": 5 },
        "desbloquea": ["riego_corredor_verde"]
      },
      {
        "text": "Con dos macetas va servido.",
        "effects": { "people": -15, "money": 10, "tourism": -5 }
      }
    ]
  },
  {
    "id": "zbe_cartuja",
    "title": "Cartuja respira, o eso dice el cartel",
    "description": "La Zona de Bajas Emisiones de la Cartuja divide a oficinas, universidades y repartidores: todos quieren aire limpio, pero nadie quiere llegar tarde.",
    "options": [
      {
        "text": "Multas desde el primer dia.",
        "effects": { "people": -10, "money": 15, "tourism": -10 },
        "desbloquea": ["sensores_no2_cartuja"]
      },
      {
        "text": "Avisos, sensores y mucha pedagogia.",
        "effects": { "people": 10, "money": -5, "tourism": 5 }
      }
    ]
  },
  {
    "id": "colegios_limpios",
    "title": "El mocho ilustrado",
    "description": "Los colegios publicos estrenan nuevo modelo de limpieza, maquinaria y casi cuatrocientos trabajadores. Los pupitres ya no se pegan al codo.",
    "options": [
      {
        "text": "Limpieza diaria y controles serios.",
        "effects": { "people": 15, "money": -10, "religion": 5 }
      },
      {
        "text": "Que cada clase barra su reino.",
        "effects": { "people": -20, "money": 10 }
      }
    ]
  },
  {
    "id": "lipasam_presupuesto_record",
    "title": "Lipasam premium",
    "description": "El presupuesto de limpieza bate record y alguien propone papeleras inteligentes que avisen antes de que el centro huela a despedida de soltero.",
    "options": [
      {
        "text": "Papeleras con sensores y cuadrillas extra.",
        "effects": { "people": 10, "money": -15, "tourism": 10 },
        "desbloquea": ["papeleras_quejicas"]
      },
      {
        "text": "Una escoba y fe municipal.",
        "effects": { "people": -15, "money": 10, "tourism": -5 }
      }
    ]
  },
  {
    "id": "cruceros_megayates",
    "title": "Megayates en Delicias",
    "description": "La nueva terminal quiere atraer cruceros y megayates de alto poder adquisitivo. El rio se prepara para oler a protector solar caro.",
    "options": [
      {
        "text": "Recibelos con alfombra roja.",
        "effects": { "money": 20, "tourism": 20, "people": -15 },
        "desbloquea": ["souvenirs_delicias"]
      },
      {
        "text": "Limita atraques y protege el muelle.",
        "effects": { "people": 10, "money": -10, "tourism": -15 }
      }
    ]
  },
  {
    "id": "aeropuerto_record",
    "title": "San Pablo no cabe",
    "description": "El aeropuerto viene de ano record y las maletas ya hacen cola antes que los pasajeros. Se propone ampliar servicios y conexiones.",
    "options": [
      {
        "text": "Mas rutas, mas taxis, mas caos controlado.",
        "effects": { "money": 15, "tourism": 15, "people": -10 },
        "desbloquea": ["colas_san_pablo"]
      },
      {
        "text": "Primero que funcione la cinta.",
        "effects": { "people": 10, "money": -5, "tourism": -10 }
      }
    ]
  },
  {
    "id": "proteccion_bic_total",
    "title": "Patrimonio hasta en el pomo",
    "description": "Urbanismo quiere reforzar la proteccion de entornos BIC en todo el Conjunto Historico. Hasta cambiar una reja podria necesitar tres sellos y una venia.",
    "options": [
      {
        "text": "Protege cada piedra.",
        "effects": { "religion": 15, "people": -5, "money": -10, "tourism": 5 },
        "desbloquea": ["licencia_para_pomo"]
      },
      {
        "text": "Menos papeleo para reformar.",
        "effects": { "religion": -10, "people": 10, "money": 10 }
      }
    ]
  },
  {
    "id": "efeso_formacion",
    "title": "Curso con practicas y cafelito",
    "description": "El programa Efeso ofrece formacion, practicas y acompanamiento laboral para personas desempleadas. La burocracia pide tres fotocopias y esperanza.",
    "options": [
      {
        "text": "Amplia plazas y orientadores.",
        "effects": { "people": 15, "money": -10 }
      },
      {
        "text": "Que se apunten online, si pueden.",
        "effects": { "people": -10, "money": 5 }
      }
    ]
  },
  {
    "id": "agua_regenerada_guadalquivir",
    "title": "El agua que vuelve",
    "description": "Agricultores del entorno del Guadalquivir piden usar agua regenerada de Sevilla. La ciudad mira sus depuradoras con repentina solemnidad.",
    "options": [
      {
        "text": "Cede agua regenerada al campo.",
        "effects": { "people": 10, "money": 10, "religion": 5, "tourism": -5 },
        "desbloquea": ["arrozales_depurados"]
      },
      {
        "text": "Guardala para parques y baldeos.",
        "effects": { "people": -5, "money": -5, "tourism": 5 }
      }
    ]
  },
  {
    "id": "escenario_flotante_guadalquivir",
    "title": "Concierto sobre el rio",
    "description": "Una plataforma quiere montar un escenario flotante en el Guadalquivir. Los fans aplauden; Capitania pregunta si el bombo tiene chaleco.",
    "options": [
      {
        "text": "Que cante hasta la Torre del Oro.",
        "effects": { "people": 10, "money": 15, "tourism": 10, "religion": -5 }
      },
      {
        "text": "El rio no es un tablao.",
        "effects": { "people": -10, "money": -5, "tourism": -10, "religion": 5 }
      }
    ]
  },
  {
    "id": "riego_corredor_verde",
    "title": "El corredor pide beber",
    "description": "El nuevo corredor verde prende bien, pero mantenerlo vivo en Sevilla Este exige riego, sensores y una fe botanica impropia de agosto.",
    "requisitos": ["corredor_verde_este"],
    "options": [
      {
        "text": "Riego eficiente y mantenimiento.",
        "effects": { "people": 10, "money": -10, "tourism": 5 }
      },
      {
        "text": "Que sobreviva el mas fuerte.",
        "effects": { "people": -15, "money": 5, "tourism": -5 }
      }
    ]
  },
  {
    "id": "sensores_no2_cartuja",
    "title": "El oraculo del NO2",
    "description": "Los sensores de la Cartuja empiezan a decidir cuando se multa. Los conductores miran el aire como quien mira el parte de lluvia en romeria.",
    "requisitos": ["zbe_cartuja"],
    "options": [
      {
        "text": "Publica los datos en tiempo real.",
        "effects": { "people": 10, "money": -5, "tourism": 5 }
      },
      {
        "text": "Que el sensor hable solo al cajero.",
        "effects": { "people": -15, "money": 15, "tourism": -5 }
      }
    ]
  },
  {
    "id": "papeleras_quejicas",
    "title": "La papelera te vigila",
    "description": "Las papeleras inteligentes mandan avisos, pero una se ha puesto intensa y notifica cada servilleta como emergencia historica.",
    "requisitos": ["lipasam_presupuesto_record"],
    "options": [
      {
        "text": "Ajusta sensores y rutas.",
        "effects": { "people": 10, "money": -5, "tourism": 5 }
      },
      {
        "text": "Silencia las papeleras dramaticas.",
        "effects": { "people": -10, "money": 5, "tourism": -5 }
      }
    ]
  },
  {
    "id": "souvenirs_delicias",
    "title": "Imanes en el muelle",
    "description": "Tras la llegada de megayates, el Paseo de las Delicias se llena de puestos con imanes, abanicos y una camiseta que pone 'I love Triana Premium'.",
    "requisitos": ["cruceros_megayates"],
    "options": [
      {
        "text": "Reserva espacio para comercio local.",
        "effects": { "people": 10, "money": 5, "tourism": -5 }
      },
      {
        "text": "Deja que mande el souvenir.",
        "effects": { "money": 15, "tourism": 10, "people": -15 }
      }
    ]
  },
  {
    "id": "colas_san_pablo",
    "title": "La cinta numero tres",
    "description": "El aeropuerto recibe mas pasajeros, pero la cinta de equipajes numero tres desarrolla personalidad propia y entrega maletas por bulerias.",
    "requisitos": ["aeropuerto_record"],
    "options": [
      {
        "text": "Refuerza personal y equipajes.",
        "effects": { "people": 10, "money": -10, "tourism": 10 }
      },
      {
        "text": "Pon un cartel de 'paciencia'.",
        "effects": { "people": -15, "money": 5, "tourism": -10 }
      }
    ]
  },
  {
    "id": "licencia_para_pomo",
    "title": "Expediente para un pomo",
    "description": "La nueva proteccion patrimonial funciona tan bien que un vecino pide permiso para cambiar un pomo y recibe un informe con bibliografia.",
    "requisitos": ["proteccion_bic_total"],
    "options": [
      {
        "text": "Ventanilla rapida para reformas menores.",
        "effects": { "people": 10, "money": 5, "religion": -5 }
      },
      {
        "text": "Cada pomo tiene su historia.",
        "effects": { "religion": 10, "people": -10, "money": -5 }
      }
    ]
  },
  {
    "id": "arrozales_depurados",
    "title": "Arroz con trazabilidad",
    "description": "El agua regenerada llega al campo y ahora todos preguntan si el arroz viene con certificado, analitica y sello municipal.",
    "requisitos": ["agua_regenerada_guadalquivir"],
    "options": [
      {
        "text": "Controles publicos y comunicacion clara.",
        "effects": { "people": 10, "money": -5, "religion": 5 }
      },
      {
        "text": "No expliques nada, que fluya.",
        "effects": { "people": -15, "money": 10, "religion": -5 }
      }
    ]
  }
]
```
