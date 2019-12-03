import requests


def main():
    """
    Cria uma caixa postal
    :param data: dicionário com os dados da caixa postal.
    """
    try:
        url_login = "http://flnif004dev.nexxera.com:6085/skyadmin/login"
        data_user = {
            "username": "Adm_cartoes",
            "password": "cartoes2019"
        }

        with requests.Session() as session:
            response = session.post(url=url_login, data=data_user)
            print(response.status_code)
            print(response.content)

            if response.status_code != 200:
                raise Exception("Erro ao acessar a caixa postal {}".format(response.content))

            try:
                skyline_url = 'http://flnif004dev.nexxera.com:6085/skyadmin/users'
                print(skyline_url)
                data = {"name": "testando654645"}
                ret = session.post(url=skyline_url, data=data)
                print(ret.status_code)
                print(ret.content)

                if ret.status_code != 200:
                    raise Exception("Erro ao criar caixa postal {}".format(ret.content))

            except ConnectionError as ccn:
                raise Exception('Erro ao criar caixa postal no Commander.'.format(ccn))

    except Exception as err:
        raise Exception("Erro ao criar caixa postal {}".format(err))


if __name__ == "__main__":
    main()
