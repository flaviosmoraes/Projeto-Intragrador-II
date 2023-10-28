function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function postoResiduos(id){
    dialog.showModal()
}

const csrftoken = getCookie('csrftoken');
const dialog = document.querySelector('dialog');
var btnExp = document.querySelector('.btn-expand');
const dialogBtn = document.getElementById('dialog-btn');

var recycleIcon = L.icon({
    iconUrl: '/static/mapa/img/recycle.svg',
    iconSize: [25, 43],
    iconAnchor: [22, 38],
    popupAnchor: [-3, -76],
    shadowUrl: '/static/mapa/img/marker-shadow.png'
});

var map = L.map('map', {
    maxZoom: 18,
    minZoom: 12,
    maxBounds: [
        //south west
        [-23.38267173019097, -45.567130688617944],
        //north east
        [-23.050520884822685, -46.22160582925989]
        ], 
}).setView([-45.89630216400873, -23.19709799312104], 12);

map.panTo(new L.LatLng(-23.21974444522734, -45.89177857753719));

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a>'
}) .addTo(map);

var xhr = new XMLHttpRequest();
xhr.open('POST', 'getGeoJSON', true);
xhr.setRequestHeader("X-CSRFToken", csrftoken);
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        L.geoJSON(data, {
            pointToLayer: function (feature, latlng) {
                var popupContent = `
                    <b>${feature.properties.nome_posto}</b><br>
                    ${feature.properties.endereco_completo}<br>
                    <b>Quantidade de resíduos a recolher:</b> ${feature.properties.total_a_recolher} Kg<br><br>
                    <b>Clique para mais detalhes!</b>
                `;

                var marker = L.marker(latlng, {icon: recycleIcon}).bindPopup(popupContent, {
                    maxWidth: 600,
                    offset: [-5, 40],
                    closeButton: false
                });

                marker.on('mouseover', function () {
                    this.openPopup();
                });

                marker.on('mouseout', function () {
                    this.closePopup();
                });

                marker.on('click', function(){
                    postoResiduos()
                })
                return marker;
            }
        }).addTo(map);
    }
};
xhr.send();

btnExp.addEventListener('click', function(){
    setTimeout(() => {
        map.panTo(new L.LatLng(-23.21974444522734, -45.89177857753719));
    }, 1000);
})

dialogBtn.addEventListener('click', function () {
    dialog.close();
});