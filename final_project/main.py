from final_project.settings import AppSettingsError, SettingsLoad
from final_project.console import ConsoleApp, ConsoleView


def main() -> int:
    settings_loader = SettingsLoad()
    view = ConsoleView()

    try:
        settings = settings_loader.load_setting()
    except AppSettingsError as error:
        view.print_invalid_settings(error)
        return 1
    else:
        ConsoleApp(settings, view=view).run()

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
