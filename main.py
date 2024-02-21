import time
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder

Window.size = (800, 600) #tamanho da tela

class TesteReacaoApp(App):
    i = 0 #definido fora para que possa ser usando dentro das funcoes
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.listaReacoes = [] #cria a lista de reacoes

    def build(self):
        layout = GridLayout(cols=1, padding=10) #define layout
        self.label = Label(text="Olá!\n", halign='center', valign='middle') #organiza o label de texto
        layout.add_widget(self.label) #cria o label de texto
        Clock.schedule_once(self.texto_dois, 1.5) #roda o prox texto apos 1.5seg
        return layout

    def texto_dois(self, dt):
        self.label.text = "" #limpa o label de texto
        self.label.text += "Nós vamos testar seu tempo de reação.\n" #escreve no label de texto
        Clock.schedule_once(self.texto_tres, 2) #roda o prox texto apos 2s

    def texto_tres(self, dt):
        self.label.text = "" #limpa o label de texto
        self.label.text += "Pressione o botão o mais rápido que puder quando aparecer a palavra: PIKACHU\n" #escreve no label de texto
        Clock.schedule_once(self.inicializador, 2) #roda a func inicializador apos 2seg
        
    def inicializador(self, dt):
        self.label.text = "" #limpa o label de texto
        self.label.text += "Pronto? E lá vamos nós! (pressione o botão)\n" #escreve no label de texto
        self.button = Button(text=" ", size_hint=(None, None), size=(150, 90), pos=(405-75, 75)) # organiza botao
        self.button.bind(on_press=self.iniciar_teste_reacao) #chama a funcao de inicio
        self.label.add_widget(self.button) #cria o botao

    def iniciar_teste_reacao(self, instance):
        self.label.text = "" #limpa o label de texto
        self.button.unbind(on_press=self.iniciar_teste_reacao) #desvincula o botao a chamada da funcao iniciar_teste_reacao para que o botao seja usadao p/ outra coisa agora
        
        if self.i < 10: #contador de 10 vezes de testes - AJUSTAR PARA 10 DEPOIS
            self.label.text += "Prepare-se...\n" #escreve no label de texto
            Clock.schedule_once(self.inicio_pikachu, random.randint(2000,3500)/1000) #chama a funcao inicio_pikachu em um tempo aleatorio entre 2ms a 3,5ms p/ deixar aleatorio e mais desafiador
        else:
            self.resultado() #apos acabar o contador ele mostra o resultado
        
    inicio_tempo = 0 #cria a var inicio_tempo fora p q possa ser usada em inicio_pikachu e fim_pikachu
    
    def inicio_pikachu(self, dt):
        self.label.text = "PIKACHU\n" #escreve no label de texto
        self.inicio_tempo = time.time() #inicia o tempo
        Clock.schedule_once(self.gravar_tempoReacao, 0)
        self.button.bind(on_press=self.fim_pikachu) #ao pressionar o botao vai chamar a funcao fim_pikachu
        
    def fim_pikachu(self, dt):
        fim_tempo = time.time() #termina o tempo
        tempoReagiu = fim_tempo-self.inicio_tempo #calcula o tempo de reacao subtraindo o fim pelo inicio
        tempoReagiu = int(round(tempoReagiu*1000)) #transforma em milisegundos o tempo de reacao
        if tempoReagiu == 0: #se o tempo for 0, qr dizer q o usuario clicou antes da hora
            self.label.text = "" #limpa o label de texto
            self.label.text = "Você se precipitou! Tempo não registrado." #escreve no label de texto
        elif tempoReagiu > 800: #se o tempo for maior que 800, alguma coisa deve ter acontecido. Esse tempo nao sera registrado
            self.label.text = "" #limpa o label de texto
            self.label.text = "Se distraiu? Tempos acima de 800ms não são considerados." #escreve no label de texto
        else: #condicao normal
            self.listaReacoes.append(tempoReagiu) #salva na lista o tempo de reacao dessa iteracao
            self.label.text = "" #limpa o label de texto
            self.label.text = f"Teste n°{self.i+1} - Tempo de Reação: {self.listaReacoes[-1]} millisegundos.\n" #escreve no label de texto
        Clock.schedule_once(self.iniciar_teste_reacao, 2) #conta 2s p dps iniciar novamente o teste
        self.i += 1 #add 1 no contador de vezes de fzr testes
            
    def gravar_tempoReacao(self, dt): #tempo de reacao
        pass
    
    def resultado(self):
        # print(self.listaReacoes) -> Printa no terminal a lista de reacoes
        temposReacao_str = ', '.join(map(str, self.listaReacoes)) #prepara a lista de reacoes para mostrar na tela
        self.tempoMedio = int(round(sum(self.listaReacoes) / len(self.listaReacoes))) #salva o tempoMedio apos calcular
        self.label.text += f"Sua média de tempo de reação é {self.tempoMedio}ms\n\n" #mostra o tempoMedio
        self.label.text += f"Tempos de reação: [{temposReacao_str}]\n\n" #mostra a lista de reacoes na tela
        
        #ifs para avaliar o tempoMedio do usuario
        if self.tempoMedio < 250:
            self.label.text += f"Parabéns! O seu tempo de reação é {250 - (self.tempoMedio)} milissegundos mais rápido que a média humana!\n\n"
        elif self.tempoMedio == 250:
            self.label.text += f"Boa! Seu tempo de reação foi exatamente igual ao da média humana\n\n"
        elif self.tempoMedio > 250:
            self.label.text += f"Poxa! O seu tempo de reação é {(self.tempoMedio) - 250} milissegundos mais lento que a média humana.\n\n"
            
        self.label.text += "Muito obrigado por sua participação!\n\n"
if __name__ == "__main__": #rodar o app
    TesteReacaoApp().run()