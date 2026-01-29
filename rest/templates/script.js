console.log("je suis la !");


// initialise la carte, centrée sur paris par défaut 
  const map = L.map('map').setView([48.8566, 2.3522], 13);

  // affichage de la map : mention obligatoire de openstreetmap et paramètre de zoom max pour l'user
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // les boutons 
  const btn = document.getElementById("test-api-btn");
  const result = document.getElementById("result");
  const resBorne = document.getElementById("resBorne");

  btn.addEventListener("click", async () => {
      result.textContent = "Appel en cours...";

      try {
      const response = await fetch("/api/test");
      const data = await response.json();
      // const responseBorne = await fetch("/api/bornes")
      // const dataBorne = await response.json();

      result.textContent = JSON.stringify(data["msg"], null, 2);
      // resBorne.textContent = Json.stringify(dataBorne["ad_station"])
      } catch (err) {
      result.textContent = "Erreur lors de l’appel API";
      console.error(err);
      }
  });