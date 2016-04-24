LANGUAGES = {
    'en': 'eng',
    'de': 'deu',
    'be': 'bel',
    'az': 'aze',
    'cs': 'ces',
    'hr': 'hrv',
    'hu': 'hun',
    'ru': 'rus',
    'pl': 'pol',
    'sk': 'slk',
    'sl': 'slv',
    'sq': 'sqi',
    'sr': 'srp',
    'tr': 'tur',
    'uk': 'ukr'
}


def _get_languages(languages):
    if languages is None or not len(languages):
        languages = ['en']

    supported = []
    for lang in languages:
        if lang is None or len(lang.strip()) not in [2, 3]:
            continue
        lang = lang.lower().strip()
        if len(lang) == 2:
            if lang not in LANGUAGES:
                continue
            lang = LANGUAGES.get(lang)
        supported.append(lang)

    return '+'.join(sorted(supported))
