from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
import os
from kivymd.toast import toast
from Functions import get_excel_rows, post_db, get_db, patch_db, delete_db
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty
from kivy.metrics import dp

from kivymd.uix.list import OneLineIconListItem
Window.size = (930, 580)


class Painel(MDScreen):

    pass


class CadastroTransportadora(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path,
            background_color_toolbar="#0d1117",

        )

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path: str):

        try:

            data = get_excel_rows(path)
            same_values = get_db('Transportadora', conflict=True, data=data)
            only_numbers = [item for item in same_values if item != '-']
            texto = str(only_numbers)

            if len(same_values) == 0:
                for value in data:
                    data_json = {
                        'ID': value[0],
                        'nome': value[1],
                        'peso_icial': value[2],
                        'peso_final': value[3],
                        'cep_inicial': value[4],
                        'cep_final': value[5],
                        'prazo': value[6],
                        'estado': value[7],
                        'cidade': value[8],
                        'regiao': value[9],
                        'frete': value[10],
                        'frete_min': value[11],
                        'tac': value[12],
                        'gris': value[13],
                        'advalorem': value[14],
                        'pedagio': value[15],
                        'tas': value[16],
                        'icms': value[17],
                        'outros': value[18]
                    }
                    post_db('Transportadora', data_json)

            else:
                snackbar = Snackbar(
                    text="ERRO! ID's repetidos: " + texto,
                    pos_hint={"center_y": .82},
                    snackbar_animation_dir="Left",
                    size_hint_x=.35,
                )
                snackbar.open()

        except:
            Snackbar(
                text="Arquivos Suportados: XSLX",
                size_hint_x=.3,
                pos_hint={"center_y": .82},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()

        self.exit_manager()

    def exit_manager(self, *args):

        self.manager_open = False
        self.file_manager.close()
    pass


class InserirTransportadora(MDScreen):

    def insert_into(self):
        try:
            post_db('Transportadora', {
                'ID': get_db('Transportadora', last=True),
                'nome': self.ids.nome.text,
                'peso_inicial': self.ids.pinicial.text,
                'peso_final': self.ids.pfinal.text,
                'cep_inicial': self.ids.cepinicial.text,
                'cep_final': self.ids.cepfinal.text,
                'prazo': self.ids.prazo.text,
                'estado': self.ids.estado.text,
                'cidade': self.ids.cidade.text,
                'regiao': self.ids.regiao.text,
                'frete': self.ids.frete.text,
                'frete_min': self.ids.fretemin.text,
                'tac': self.ids.tac.text,
                'gris': self.ids.gris.text,
                'advalorem': self.ids.advalorem.text,
                'pedagio': self.ids.pedagio.text,
                'tas': self.ids.tas.text,
                'icms': self.ids.icms.text,
                'outros': self.ids.outros.text})
            self.ids.nome.text = ''
            self.ids.pinicial.text = ''
            self.ids.pfinal.text = ''
            self.ids.cepinicial.text = ''
            self.ids.cepfinal.text = ''
            self.ids.prazo.text = ''
            self.ids.estado.text = ''
            self.ids.cidade.text = ''
            self.ids.regiao.text = ''
            self.ids.frete.text = ''
            self.ids.fretemin.text = ''
            self.ids.tac.text = ''
            self.ids.gris.text = ''
            self.ids.advalorem.text = ''
            self.ids.pedagio.text = ''
            self.ids.tas.text = ''
            self.ids.icms.text = ''
            self.ids.outros.text = ''

            Snackbar(
                text="Cadastro Concluído!",
                size_hint_x=.3,
                pos_hint={"center_y": .82},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()
        except:
            Snackbar(
                text="Erro ao Cadastrar",
                size_hint_x=.3,
                pos_hint={"center_y": .82},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()


class EditarTransportadora(MDScreen):
    def on_enter(self):
        
        empresas = get_db('Transportadora', names=True)
        menu_items = [
            {
                "viewclass": "IconListItem",
                "text": i,
                "height": dp(56),
                "on_release": lambda x=i: self.set_item(x),
            } for i in empresas
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="bottom",
            width_mult=4,
            elevation=1,
        )
        self.menu.bind()

    def set_item(self, text_item):
        self.text_name = text_item
        try:
        
            empresa = get_db('Transportadora', find_name=text_item)
            self.ids.drop_item.set_item(text_item)
            self.ids.pinicial.text = str(empresa['peso_inicial'])
            self.ids.pfinal.text = str(empresa['peso_final'])
            self.ids.cepinicial.text = str(empresa['cep_inicial'])
            self.ids.cepfinal.text = str(empresa['cep_final'])
            self.ids.prazo.text = str(empresa['prazo'])
            self.ids.estado.text = str(empresa['estado'])
            self.ids.cidade.text = str(empresa['cidade'])
            self.ids.regiao.text = str(empresa['regiao'])
            self.ids.frete.text = str(empresa['frete'])
            self.ids.fretemin.text = str(empresa['frete_min'])
            self.ids.tac.text = str(empresa['tac'])
            self.ids.gris.text = str(empresa['gris'])
            self.ids.advalorem.text = str(empresa['advalorem'])
            self.ids.pedagio.text = str(empresa['pedagio'])
            self.ids.tas.text = str(empresa['tas'])
            self.ids.icms.text = str(empresa['icms'])
            self.ids.outros.text = str(empresa['outros'])

            self.menu.dismiss()
        except:
            Snackbar(
                text="Empresa Inexistente",
                size_hint_x=.3,
                pos_hint={"center_y": .8},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()
    def edit_transp(self):
        try:
            item_key = get_db('Transportadora', find_key_by_name=self.text_name)
            dict_dados = {
                'peso_inicial': self.ids.pinicial.text,
                'peso_final': self.ids.pfinal.text,
                'cep_inicial': self.ids.cepinicial.text,
                'cep_final': self.ids.cepfinal.text,
                'prazo': self.ids.prazo.text,
                'estado': self.ids.estado.text,
                'cidade': self.ids.cidade.text,
                'regiao': self.ids.regiao.text,
                'frete': self.ids.frete.text,
                'frete_min': self.ids.fretemin.text,
                'tac': self.ids.tac.text,
                'gris': self.ids.gris.text,
                'advalorem': self.ids.advalorem.text,
                'pedagio': self.ids.pedagio.text,
                'tas': self.ids.tas.text,
                'icms': self.ids.icms.text,
                'outros': self.ids.outros.text}
            
            patch_db(f'Transportadora/{item_key}', dict_dados)
            self.ids.pinicial.text = ''
            self.ids.pfinal.text = ''
            self.ids.cepinicial.text = ''
            self.ids.cepfinal.text = ''
            self.ids.prazo.text = ''
            self.ids.estado.text = ''
            self.ids.cidade.text = ''
            self.ids.regiao.text = ''
            self.ids.frete.text = ''
            self.ids.fretemin.text = ''
            self.ids.tac.text = ''
            self.ids.gris.text = ''
            self.ids.advalorem.text = ''
            self.ids.pedagio.text = ''
            self.ids.tas.text = ''
            self.ids.icms.text = ''
            self.ids.outros.text = ''

            Snackbar(
                text="Atualizado com Sucesso!",
                size_hint_x=.3,
                pos_hint={"center_y": .8},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()

        except:
            Snackbar(
                text="Selecione uma Empresa",
                size_hint_x=.3,
                pos_hint={"center_y": .8},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()
    def delete_transp(self):
        
        try:
            name_key = get_db('Transportadora', find_key_by_name=self.text_name)
            delete_db(f'Transportadora/{name_key}')

            Snackbar(
                text="Excluído com Sucesso",
                size_hint_x=.3,
                pos_hint={"center_y": .8},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()
        
        except:

            Snackbar(
                text="Erro ao Deletar",
                size_hint_x=.3,
                pos_hint={"center_y": .8},
                snackbar_animation_dir="Left",
                elevation=0,

            ).open()
        



class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class Program(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return


Program().run()
