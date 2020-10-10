var api = location.origin + '/api/';
var data = [];
var coords = [-84.870, 38.903];
var markers = [];
var popups = [];
var styles = ['mapbox://styles/mapbox/dark-v10', 'mapbox://styles/mapbox/streets-v11', 'mapbox://styles/mapbox/light-v10', 'mapbox://styles/bufo333/ckfgvmau920nc19qc0y1ah18l',
    'mapbox://styles/bufo333/ckfgwf2ym2c8q19pp8c7804lp', 'mapbox://styles/mapbox/satellite-v9', 'mapbox://styles/bufo333/ckfidnufh2lvl19p7bsgl7z3e'
];


function domap(mylat, mylon, sttp) {
    if (data.length >0 && mylat != 'S000 00.000' && mylon != 'W000 00.000' ) {
        coords = Get_Coords(mylat, mylon).reverse();
    }
    mapboxgl.accessToken = 'pk.eyJ1IjoiYnVmbzMzMyIsImEiOiJja2ZqMDEwNzEwMHRoMnFxcnJmdzhveTF6In0.UarZo_wKm5LmPeZXJYDRPw';
    var map = new mapboxgl.Map({
        container: 'map',
        style: sttp,
        zoom: 2,
        center: coords,
    });
    var home = new mapboxgl.Marker({
            color: 'red'
        })
        .setLngLat(coords)
        .addTo(map);
    var homepop = new mapboxgl.Popup()
    homepop.setHTML('<small><strong> <p>' +
        '<BR/>Lat  :' + coords[1] +
        '<BR/>Lon  :' + coords[0] +
        '</P></small></strong>');
    home.setPopup(homepop);
    var i = -1;
    data.forEach(function (contact) {
        i++
        if (contact['lat'] != 'S000 00.000' && contact['lon'] != 'W000 00.000' ) {
            var marker = new mapboxgl.Marker()
            var values = Get_Coords(contact['lat'], contact['lon']).reverse();
            if (values[0] && values[1]) {
                marker.setLngLat(values)
                marker.addTo(map);
            }
            var popup = new mapboxgl.Popup()
                .setHTML('<small><strong> <p>' +
                    'Band  :' + contact['band'] +
                    '<BR/>Band RX  :' + contact['band_rx'] +
                    '<BR/>call  :' + contact['call'] +
                    '<BR/>Cont  :' + contact['cont'] +
                    '<BR/>Country  :' + contact['country'] +
                    '<BR/>CQZ   :' + contact['cqz'] +
                    '<BR/>Distance   :' + contact['distance'] +
                    '<BR/>DXCC  :' + contact['dxcc'] +
                    '<BR/>email  :' + contact['email'] +
                    '<BR/>Grid Square  :' + contact['gridsquare'] +
                    '<BR/>ITUZ   :' + contact['ituz '] +
                    '<BR/>Lat  :' + contact['lat'] +
                    '<BR/>Lon  :' + contact['lon'] +
                    '<BR/>Mode  :' + contact['mode'] +
                    '<BR/>Name  :' + contact['name'] +
                    '<BR/>QSO Date   :' + contact['qso_date'] +
                    '<BR/>QSO Date Off   :' + contact['qso_date_off'] +
                    '<BR/>QTH  :' + contact['qth'] +
                    '<BR/>Rst Sent  :' + contact['rst_sent'] +
                    '<BR/>Rst Received  :' + contact['rst_rcvd'] +
                    '<BR/>Station Callsign  :' + contact['station_callsign'] +
                    '<BR/>Time Off   :' + contact['time_off'] +
                    '<BR/>Time On  :' + contact['time_on'] +
                    '<BR/>Number: ' + i +
                    '</P></small></strong>');
            popups.push(popup);
            markers.push(marker);
            marker.setPopup(popup);
        }
    });

}


function changeTheme() {
    domap(data, styles[document.getElementById("Themes").value]);
}

function Get_Coords(lat, lon) {
    var mylat = {
        then: function (resolve, _reject) {
            var tmplat = lat;
            if (lat[0] == 'S') {
                tmplat = lat[0].replace('S', '')
            } else {
                tmplat = lat.replace('N', '');
            }
            var [d, m] = tmplat.split(' ')
            if (d[0] == '-') {
                tmplat = Number(d) - (Number(m) / 60);
            } else {
                tmplat = Number(d) + (Number(m) / 60);
            }
            return tmplat;
        }
    };
    var mylon = {
        then: function (resolve, _reject) {
            var tmplon = lon;
            if (lon[0] == 'W') {
                tmplon = lon.replace('W', '-');
            } else {
                tmplon = lon.replace('E', '');
            }
            var [d, m] = tmplon.split(' ')
            if (d[0] == '-') {
                tmplon = Number(d) - (Number(m) / 60);
            } else {
                tmplon = Number(d) + (Number(m) / 60);
            }
            return tmplon;
        }
    };
    return [mylat.then(), mylon.then()];
}

async function getdata() {
    return await $.ajax({
        type: "POST",
        dataType: "JSON",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            'Email': JSON.parse(document.getElementById('datadiv').dataset.user).email
        }),
        url: api,
        success: function (results) {
            data = results;
        }

    });

}
getdata().then((data) => {
    console.log(data[0]);
    domap(data[0]['my_lat'] || data[0]['MY_LAT'], data[0]['my_lon'] || data[0]['MY_LON'], styles[JSON.parse(document.getElementById('datadiv').dataset.user).theme]);
});   
