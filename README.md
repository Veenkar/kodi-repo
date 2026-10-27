# Veenkar Kodi repository

Kodi add-on repository with a maintained **CanalPLUS-VOD** (`plugin.video.canalplusvod`). The original repo (mbebe/blomqvist) hasn't been updated since 2024.

## Installation (PL)

1. Kodi → Ustawienia → System → Dodatki → włącz **Nieznane źródła**.
2. Pobierz [`repository.veenkar-1.0.0.zip`](https://raw.githubusercontent.com/Veenkar/kodi-repo/main/zips/repository.veenkar/repository.veenkar-1.0.0.zip) i zainstaluj: Dodatki → **Zainstaluj z pliku zip**.
3. Dodatki → **Zainstaluj z repozytorium** → *Veenkar Repository* → Dodatki wideo → **CanalPLUS-VOD**.

Wymagane: `inputstream.adaptive` i Widevine (inputstreamhelper zaproponuje instalację przy pierwszym odtworzeniu).

### Logowanie (passId)

Logowanie hasłem w Canal+ przeszło na Okta z ochroną antybotową, więc dodatek loguje się tokenem z przeglądarki:

1. Zaloguj się na [canalplus.com](https://www.canalplus.com/pl/) w przeglądarce na komputerze.
2. F12 → **Sieć/Network** → w filtrze wpisz `createToken` → odśwież stronę (F5).
3. Wybierz żądanie `createToken`, którego **Payload** zawiera tylko `portailId, media, vect, passIdType, noCache, passId` (bez `analytics`/`trackingPub`). Skopiuj wartość **passId** (ok. 180 znaków, zaczyna się od `PL=`).
4. Zamknij kartę **bez wylogowywania** (wylogowanie unieważnia passId).
5. Kodi → CanalPLUS-VOD → Ustawienia → wklej do **passId z przeglądarki**, włącz **Zaloguj do serwisu**.

Wklejasz tylko raz – dodatek sam odświeża token.

### Jakość obrazu

Kodi używa Widevine L3 (programowego). Canal+ wydaje mu klucze tylko do SD (do 540p), więc 720p/1080p dają dźwięk bez obrazu. Ustawienie **Maks. rozdzielczość** domyślnie 640p. Wyższej jakości nie da się uzyskać w Kodi; HD jest dostępne w przeglądarce na Windows albo w oficjalnej aplikacji na certyfikowanym urządzeniu.

## Installation (EN)

Install `repository.veenkar-1.0.0.zip` via *Add-ons → Install from zip file* (enable *Unknown sources* first), then install **CanalPLUS-VOD** from *Veenkar Repository*. Login: paste the `passId` from the logged-in `createToken` request on canalplus.com (DevTools → Network → Payload) into the add-on settings. Widevine L3 gets SD (≤540p) only.

Add-on source: <https://github.com/Veenkar/blomqvist_srcs/tree/canalplus-1.8.0.0> · upstream PR: <https://github.com/mbebe/blomqvist_srcs/pull/23>

## Maintenance

Add the new zip as `zips/<id>/<id>-<version>.zip`, run `python update_repo.py` (regenerates `addons.xml`, its MD5 and the add-on art), commit and push.
