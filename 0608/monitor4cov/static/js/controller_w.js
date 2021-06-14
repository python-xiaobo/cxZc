function getTime() {
    $.ajax({
        url: "/time", success: function (time_str) {
            $("#tim").html(time_str)
        }
    })
}

function get_lw_data() {
    $.ajax({
        url: "/w", success: function (data) {
            ecc_world_option.series[0].data = data.data;
            ecc_world.setOption(ecc_world_option)
        }
    })
}

function get_rw_data() {
    $.ajax({
        url: "/r", success: function (data) {
            legenddata = data.data;
            var source = [["Country", "Confirmed", "SQRT", "Dead"]];
            var data = [];
            for (var i = 0; i < legenddata.length; i++) {
                arr = [];
                arr.push(legenddata[i].name);
                if (i != 10) {
                    data.push(legenddata[i].name)
                } else {
                    data.push("")
                }
                arr.push(legenddata[i].Confirmed);
                arr.push(Math.sqrt(legenddata[i].Confirmed));
                arr.push(legenddata[i].Dead);
                source.push(arr)
            }
            ec_world_option.dataset.source = source;
            ec_world_option.legend.data = data;
            ec_world.setOption(ec_world_option)
        }
    })
}

getTime();
get_lw_data();
get_rw_data();
setInterval(getTime, 1000);
window.addEventListener("resize", function () {
    ecc_world.resize();
    ec_world.resize()
});