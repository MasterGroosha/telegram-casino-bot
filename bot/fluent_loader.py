from pathlib import Path

from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization(language: str) -> FluentLocalization:
    """
    Loads FTL files for chosen language
    :param language: language name, as passed from configuration outside
    :return: FluentLocalization object with loaded FTL files for chosen language
    """

    # Check "locales" directory on the same level as this file
    locales_dir = Path(__file__).parent.joinpath("locales")
    if not locales_dir.exists():
        err = '"locales" directory does not exist'
        raise FileNotFoundError(err)
    if not locales_dir.is_dir():
        err = '"locales" is not a directory'
        raise NotADirectoryError(err)

    locales_dir = locales_dir.absolute()
    locale_dir_found = False
    for directory in Path.iterdir(locales_dir):
        if directory.stem == language:
            locale_dir_found = True
            break
    if not locale_dir_found:
        err = f'Directory for "{language}" locale not found'
        raise FileNotFoundError(err)

    locale_files = list()
    for file in Path.iterdir(Path.joinpath(locales_dir, language)):
        if file.suffix == ".ftl":
            locale_files.append(str(file.absolute()))
    l10n_loader = FluentResourceLoader(str(Path.joinpath(locales_dir, "{locale}")))

    return FluentLocalization([language], locale_files, l10n_loader)
