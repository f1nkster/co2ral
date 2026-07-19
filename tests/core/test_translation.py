from locales.translation import TRANSLATION_DICT


def test__translations__same_keys_in_all_languages():
    """GIVEN the translation dictionary
    WHEN the key sets of the languages are compared
    THEN they are identical, so no label falls back to a missing key at runtime
    """
    german_keys = set(TRANSLATION_DICT["de"])
    english_keys = set(TRANSLATION_DICT["en"])

    assert german_keys == english_keys, f"only de: {german_keys - english_keys}, only en: {english_keys - german_keys}"


def test__translations__no_empty_values():
    """GIVEN the translation dictionary
    WHEN all values are inspected
    THEN none of them is empty
    """
    for lang, dictionary in TRANSLATION_DICT.items():
        for key, value in dictionary.items():
            assert value.strip(), f"empty translation for {key} in {lang}"
