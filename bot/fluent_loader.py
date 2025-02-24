from pathlib import Path

from fluent.runtime import FluentLocalization, FluentResourceLoader


def get_fluent_localization() -> FluentLocalization:
    # Access "locale/current" dir
    real_locale_dir = Path(__file__).parent.joinpath("locale", "current")
    # Find all subdirectories.
    real_languages_subdirs: list = [d for d in real_locale_dir.iterdir() if d.is_dir()]
    # There must be at least one subdirectory inside. Ideally – only one.
    if len(real_languages_subdirs) == 0:
        raise RuntimeError("No languages found in the 'current' directory.")
    # Select the first subdir if there are multiple subdirectories inside.
    selected_language_dir = real_languages_subdirs[0]

    # Find all .ftl files inside the selected language directory
    ftl_files = [f.name for f in selected_language_dir.iterdir() if f.is_file() and f.suffix == ".ftl"]
    if len(ftl_files) == 0:
        raise RuntimeError(f"No .ftl files found in the {selected_language_dir.name} directory.")

    # Now form Fluent-compatible path and create Fluent objects.
    locale_dir = real_locale_dir.joinpath("{locale}")
    loader = FluentResourceLoader(str(locale_dir.absolute()))
    return FluentLocalization([selected_language_dir.name], ftl_files, loader)
