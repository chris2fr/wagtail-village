Le bandeau de Lettre d’information et Réseaux Sociaux est géré grâce à une balise `include` à insérer dans le bloc `follow_newsletter_social_media` dans le fichier `base.html`.

```{.django}
<!-- <votre_app>/templates/<votre_app>/base.html -->
{% extends "django_design_system/base.html" %}

<!-- [...] -->
{% block follow_newsletter_social_media %}
  {% include "django_design_system/follow.html" %}
{% endblock follow_newsletter_social_media %}

```

Il est alors possible de personnaliser la description de la lettre d’information, l’URL d’inscription ainsi que les réseaux sociaux via la configuration du site dans l’administration de Django.
`
- `<a class="design-system-link design-system-icon-external-link-line design-system-link--icon-right design-system-link--lg" href="https://www.systeme-de-design.gouv.fr/elements-d-interface/composants/pied-de-page" target="_blank" rel="noopener noreferrer">
        Voir la page de documentation du composant sur le Système de Design de l’État
        <span class="design-system-sr-only">Ouvre une nouvelle fenêtre</span>
  </a>`
- `<a class="design-system-link design-system-icon-external-link-line design-system-link--icon-right design-system-link--lg" href="https://main--ds-gouv.netlify.app/example/component/footer/" target="_blank" rel="noopener noreferrer">
        Voir la page d’exemple du Système de Design de l’État
        <span class="design-system-sr-only">Ouvre une nouvelle fenêtre</span>
  </a>

## Classes pour les boutons des réseaux sociaux

- `design-system-btn--dailymotion`
- `design-system-btn--facebook`
- `design-system-btn--github`
- `design-system-btn--instagram`
- `design-system-btn--linkedin`
- `design-system-btn--mastodon`
- `design-system-btn--snapchat`
- `design-system-btn--telegram`
- `design-system-btn--threads`
- `design-system-btn--tiktok`
- `design-system-btn--twitch`
- `design-system-btn--twitter`
- `design-system-btn--twitter-x`
- `design-system-btn--vimeo`
- `design-system-btn--youtube`

## Personnaliser
Il est possible de le remplacer par votre propre bloc pour étendre ses capacités (par exemple pour n’afficher qu’un des deux blocs ou pour inclure le champ d’adhésion directement dans le bandeau.)

```{.django}
<!-- <votre_app>/templates/<votre_app>/base.html -->
{% extends "django_design_system/base.html" %}

<!-- [...] -->
{% block follow_newsletter_social_media %}
  {% include "<votre_app>/blocks/follow.html" %}
{% endblock follow_newsletter_social_media %}

```

```{.django}
<!-- <votre_app>/templates/<votre_app>/blocks/follow.html -->
{% extends "django_design_system/follow.html" %}
{% block follow_newsletter %}
  <div class="design-system-col-12">
      <div class="design-system-follow__newsletter">
          <div>
              <h2 class="design-system-h5">Abonnez-vous à notre lettre d’information</h2>
              <p class="design-system-text--sm">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas varius tortor nibh, sit amet tempor nibh finibus et.</p>
          </div>
          <div>
              <form action="">
                  <div class="design-system-input-group">
                      <label class="design-system-label" for="newsletter-email">
                          Votre adresse électronique (ex. : nom@domaine.fr)
                      </label>
                      <div class="design-system-input-wrap design-system-input-wrap--addon">
                          <input class="design-system-input" title="Votre adresse électronique (ex. : nom@domaine.fr)" autocomplete="email" attributes="[object Object]" aria-describedby="newsletter-email-hint-text newsletter-email-messages" placeholder="Votre adresse électronique (ex. : nom@domaine.fr)" id="newsletter-email" type="email">
                          <button class="design-system-btn" id="newsletter-button" title="S’abonner à notre lettre d’information" type="submit">
                              S’abonner
                          </button>
                      </div>
                      <div class="design-system-messages-group" id="newsletter-email-messages" aria-live="assertive">
                      </div>
                  </div>
                  <p id="newsletter-email-hint-text" class="design-system-hint-text">En renseignant votre adresse électronique, vous acceptez de recevoir nos actualités par courriel. Vous pouvez vous désinscrire à tout moment à l’aide des liens de désinscription ou en nous contactant.</p>
              </form>
          </div>
      </div>
  </div>
{% endblock follow_newsletter %}

{% block follow_social %}
{% endblock follow_social %}
```
