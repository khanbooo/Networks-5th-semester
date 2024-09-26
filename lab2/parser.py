import re


class Parser:
    @staticmethod
    def parse(args, default_settings: dict) -> None:
        try:
            if '--' not in str(args):
                if len(args.split()) != 1:
                    raise RuntimeError('Bad input: wrong number of arguments\0')
                return
            args_list = args.split('--')[1:]
            for arg_pair in args_list:
                if len(arg_pair) == 0:
                    raise RuntimeError('Bad input: wrong number of arguments\0')

                arg_pair_splitted = arg_pair.split()
                if arg_pair_splitted[0] not in default_settings.keys():
                    raise RuntimeError('Bad input: expected argument differs from given\0')

                #pattern check
                if arg_pair_splitted[0] == 'mcast6':
                    pattern = 'ff([0-9a-f]){2}(:([0-9a-f]){4}){7}'
                    if not re.fullmatch(pattern, arg_pair_splitted[-1]):
                        raise TypeError('Incorrect IPv6 format\0')

                elif arg_pair_splitted[0] == 'mcast4':
                    pattern = "(22[4-9]|23[0-9]|)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\." \
                              "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
                    if not re.fullmatch(pattern, arg_pair_splitted[-1]):
                        raise TypeError('Incorrect IPv4 format\0')

                elif arg_pair_splitted[0] == 'port':
                    if not arg_pair_splitted[-1].isdigit():
                        raise TypeError('Incorrect symbol type for port\0')

                elif arg_pair_splitted[0] == 'ttl':
                    if not arg_pair_splitted[-1].isdigit():
                        raise TypeError('Incorrect symbol type for ttl\0')

                elif arg_pair_splitted[0] == 'group':
                    pattern = 'IPv[46]'
                    if not re.fullmatch(pattern, arg_pair_splitted[-1]):
                        raise TypeError('Incorrect IP group format\0')

                elif arg_pair_splitted[0] == 'path':
                    print(arg_pair_splitted[0], '|||', arg_pair_splitted[1])
                    pattern = r'([A-Za-z]:\\)?((?:.*\\)?)([\w\s]+\.\w+)'
                    if not re.fullmatch(pattern, arg_pair_splitted[-1]):
                        raise TypeError('Incorrect path format\0')

                default_settings[arg_pair_splitted[0]] = arg_pair_splitted[1]

        except RuntimeError as exc:
            raise RuntimeError(*exc.args)
