import pygame
import random
import sys

# Initialisation
pygame.init()

# Dimensions
LARGEUR = 1900
HAUTEUR = 1000
FPS = 90

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (218, 101, 66)
BLEU = (0, 44, 163)
VERT = (0, 200, 100)
GRIS = (92, 92, 92)
GRIS_FONCE = (160, 160, 160)

# État du jeu
etat_jeu = "intro"

# Fenêtre
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Star games")

# Fond et sprites
fond = pygame.image.load("espace.jpg")
fusee_originale = pygame.image.load("fusee.png")
fusee_originale = pygame.transform.scale(fusee_originale, (80, 140))
vaisseau_img = fusee_originale
vaisseau_img_gauche = pygame.transform.rotate(fusee_originale, 15)
vaisseau_img_droite = pygame.transform.rotate(fusee_originale, -15)

ennemi1_img = pygame.transform.scale(pygame.image.load("ennemi1.png"), (50, 120))
ennemi2_img = pygame.transform.scale(pygame.image.load("ennemi2.png"), (50, 120))
ennemi3_img = pygame.transform.scale(pygame.image.load("ennemi3.png"), (40, 120))
explosion_img = pygame.transform.scale(pygame.image.load("explosion.png"), (130, 130))

# Fonts
font = pygame.font.SysFont("arial", 30)
grand_font = pygame.font.SysFont("arial", 72)

# === Fonctions ===

def afficher_intro():
    intro_duree = 3000
    start_time = pygame.time.get_ticks()
    fond_intro = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

    while True:
        elapsed = pygame.time.get_ticks() - start_time
        if elapsed > intro_duree:
            break

        alpha = min(255, int((elapsed / intro_duree) * 255))
        intro_surface = pygame.Surface((LARGEUR, HAUTEUR))
        intro_surface.blit(fond_intro, (0, 0))

        titre = grand_font.render("STAR GAME", True, GRIS)
        auteur = font.render("Un jeu de Sanda Rakotomihamina", True, BLANC)
        titre.set_alpha(alpha)
        auteur.set_alpha(alpha)

        intro_surface.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 2 - 100))
        intro_surface.blit(auteur, (LARGEUR // 2 - auteur.get_width() // 2, HAUTEUR // 2 + 10))

        screen.blit(intro_surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def afficher_menu():
    fond_menu = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))
    screen.blit(fond_menu, (0, 0))
    titre = grand_font.render("STAR GAME", True, GRIS)
    screen.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, HAUTEUR // 2 - 150))
    bouton_commencer = pygame.Rect(LARGEUR // 2 - 180, HAUTEUR // 2, 360, 80)
    bouton_quitter = pygame.Rect(LARGEUR // 2 - 180, HAUTEUR // 2 + 100, 360, 80)
    dessiner_bouton(bouton_commencer, "COMMENCER", VERT)
    dessiner_bouton(bouton_quitter, "QUITTER", ROUGE)
    return bouton_commencer, bouton_quitter

class Projectile:
    def __init__(self, x, y):
        self.image = pygame.Surface((6, 20))
        self.image.fill(ROUGE)
        self.rect = self.image.get_rect(center=(x, y))

    def deplacer(self):
        self.rect.y -= 12

    def dessiner(self):
        screen.blit(self.image, self.rect)

class Ennemi:
    def __init__(self):
        self.type = random.choice(["type1", "type2", "type3"])
        self.image = {"type1": ennemi1_img, "type2": ennemi2_img, "type3": ennemi3_img}[self.type]
        self.rect = self.image.get_rect(topleft=(random.randint(0, LARGEUR - 60), -120))
        self.vitesse = random.randint(3, 6)

    def deplacer(self):
        self.rect.y += self.vitesse

    def dessiner(self):
        screen.blit(self.image, self.rect)

class Explosion:
    def __init__(self, x, y):
        self.image = explosion_img
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 10

    def dessiner(self):
        screen.blit(self.image, self.rect)
        self.timer -= 1

class ExplosionVaisseau:
    def __init__(self, x, y):
        self.image = explosion_img
        self.frames = 15
        self.rect = self.image.get_rect(center=(x + 30, y + 60))

    def dessiner(self):
        if self.frames > 0:
            screen.blit(self.image, self.rect)
            self.frames -= 1

def generer_ennemi():
    if random.random() < 0.02:
        ennemis.append(Ennemi())

def reinitialiser_jeu():
    global vaisseau_x, vaisseau_y, projectiles, ennemis, explosions, score, dernier_tir, game_over, explosion_vaisseau
    vaisseau_x = LARGEUR // 2
    vaisseau_y = HAUTEUR - 160
    projectiles = []
    ennemis = []
    explosions = []
    score = 0
    dernier_tir = 0
    game_over = False
    explosion_vaisseau = None

def dessiner_bouton(rect, texte, couleur, actif=False):
    if actif:
        couleur_claire = tuple(min(255, int(c * 1.2)) for c in couleur)
        ombre = rect.copy()
        ombre.move_ip(2, 2)
        pygame.draw.rect(screen, GRIS_FONCE, ombre, border_radius=15)
        pygame.draw.rect(screen, couleur_claire, rect, border_radius=15)
    else:
        pygame.draw.rect(screen, couleur, rect, border_radius=15)
    pygame.draw.rect(screen, GRIS_FONCE, rect, width=3, border_radius=15)
    txt = font.render(texte, True, NOIR)
    screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

def dessiner_boutons():
    gauche = pygame.Rect(100, HAUTEUR - 120, 140, 80)
    droite = pygame.Rect(280, HAUTEUR - 120, 140, 80)
    tirer = pygame.Rect(LARGEUR - 300, HAUTEUR - 150, 250, 120)
    dessiner_bouton(gauche, "◀", BLEU, actif=bouton_gauche_active)
    dessiner_bouton(droite, "▶", BLEU, actif=bouton_droite_active)
    dessiner_bouton(tirer, "TIRER", ROUGE, actif=bouton_tirer_active)
    return gauche, droite, tirer

def dessiner_boutons_game_over():
    recommencer = pygame.Rect(LARGEUR // 2 - 310, HAUTEUR // 2 + 50, 280, 60)
    quitter = pygame.Rect(LARGEUR // 2 + 30, HAUTEUR // 2 + 50, 280, 60)
    dessiner_bouton(recommencer, "RECOMMENCER", VERT)
    dessiner_bouton(quitter, "QUITTER", ROUGE)
    return recommencer, quitter

# Données du jeu
vaisseau_x = LARGEUR // 2
vaisseau_y = HAUTEUR - 160
vaisseau_vitesse = 8
delai_tir = 50
projectiles = []
ennemis = []
explosions = []
score = 0
dernier_tir = 0
game_over = False
explosion_vaisseau = None
bouton_gauche_active = False
bouton_droite_active = False
bouton_tirer_active = False

# Intro
afficher_intro()
etat_jeu = "menu"

# Boucle principale
clock = pygame.time.Clock()
background_y = 0
bouton_gauche = pygame.Rect(100, HAUTEUR - 90, 100, 60)
bouton_droite = pygame.Rect(230, HAUTEUR - 90, 100, 60)
bouton_tirer = pygame.Rect(LARGEUR - 200, HAUTEUR - 90, 100, 60)

while True:
    clock.tick(FPS)
    temps_actuel = pygame.time.get_ticks()
    souris_pos = pygame.mouse.get_pos()
    souris_appuyee = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if etat_jeu == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_commencer.collidepoint(event.pos):
                reinitialiser_jeu()
                etat_jeu = "jeu"
            elif bouton_quitter.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
        if etat_jeu == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_recommencer.collidepoint(event.pos):
                reinitialiser_jeu()
                etat_jeu = "jeu"
            elif bouton_quitter_game_over.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    if etat_jeu == "menu":
        bouton_commencer, bouton_quitter = afficher_menu()

    elif etat_jeu == "jeu":
        background_y += 2
        if background_y >= HAUTEUR:
            background_y = 0
        screen.blit(fond, (0, background_y))
        screen.blit(fond, (0, background_y - HAUTEUR))

        if not game_over:
            if souris_appuyee:
                bouton_gauche_active = bouton_gauche.collidepoint(souris_pos)
                bouton_droite_active = bouton_droite.collidepoint(souris_pos)
                bouton_tirer_active = bouton_tirer.collidepoint(souris_pos)
            else:
                bouton_gauche_active = bouton_droite_active = bouton_tirer_active = False

            if bouton_gauche_active and vaisseau_x > 0:
                vaisseau_x -= vaisseau_vitesse
            if bouton_droite_active and vaisseau_x < LARGEUR - 80:
                vaisseau_x += vaisseau_vitesse
            if bouton_tirer_active and temps_actuel - dernier_tir > delai_tir:
                projectiles.append(Projectile(vaisseau_x + 40, vaisseau_y))
                dernier_tir = temps_actuel

            # Vaisseau
            if bouton_gauche_active:
                screen.blit(vaisseau_img_gauche, (vaisseau_x, vaisseau_y))
            elif bouton_droite_active:
                screen.blit(vaisseau_img_droite, (vaisseau_x, vaisseau_y))
            else:
                screen.blit(vaisseau_img, (vaisseau_x, vaisseau_y))

            # Projectiles
            for p in projectiles[:]:
                p.deplacer()
                p.dessiner()
                if p.rect.bottom < 0:
                    projectiles.remove(p)

            # Ennemis
            generer_ennemi()
            for e in ennemis[:]:
                e.deplacer()
                e.dessiner()
                if e.rect.top > HAUTEUR:
                    ennemis.remove(e)

            # Collisions ennemi/projectil
            for p in projectiles[:]:
                for e in ennemis[:]:
                    if p.rect.colliderect(e.rect):
                        if p in projectiles:
                            projectiles.remove(p)
                        if e in ennemis:
                            ennemis.remove(e)
                        explosions.append(Explosion(e.rect.centerx, e.rect.centery))
                        score += 1

            # Explosions
            for exp in explosions[:]:
                exp.dessiner()
                if exp.timer <= 0:
                    explosions.remove(exp)

            # Collision vaisseau/ennemi
            vaisseau_rect = pygame.Rect(vaisseau_x, vaisseau_y, 60, 60)
            for e in ennemis:
                if e.rect.colliderect(vaisseau_rect):
                    game_over = True
                    explosion_vaisseau = ExplosionVaisseau(vaisseau_x, vaisseau_y)
                    etat_jeu = "game_over"

        # Score visible même après game over
        score_txt = font.render(f"Score : {score}", True, BLANC)
        screen.blit(score_txt, (10, 10))

        # Boutons visibles même après game over
        bouton_gauche, bouton_droite, bouton_tirer = dessiner_boutons()


    elif etat_jeu == "game_over":
        screen.blit(grand_font.render("Vous êtes mort ☠️", True, ROUGE), (LARGEUR // 2 - 285, HAUTEUR // 2 - 80))
        score_txt = font.render(f"Score : {score}", True, BLANC)
        screen.blit(score_txt, (10, 10))
        if explosion_vaisseau and explosion_vaisseau.frames > 0:
            explosion_vaisseau.dessiner()
        bouton_recommencer, bouton_quitter_game_over = dessiner_boutons_game_over()

    pygame.display.flip()
    if etat_jeu == "game_over" and explosion_vaisseau and explosion_vaisseau.frames <= 0:
        explosion_vaisseau = None
