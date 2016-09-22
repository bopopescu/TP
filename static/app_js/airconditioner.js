/**

Copyright (c) 2016, Virginia Tech
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the authors and should not be
interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.

This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the
United States Government nor the United States Department of Energy, nor Virginia Tech, nor any of their employees,
nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty,
express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe
privately owned rights.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or
otherwise does not necessarily constitute or imply its endorsement, recommendation, favoring by the United States
Government or any agency thereof, or Virginia Tech - Advanced Research Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

VIRGINIA TECH – ADVANCED RESEARCH INSTITUTE
under Contract DE-EE0006352

#__author__ = "BEMOSS Team"
#__credits__ = ""
#__version__ = "2.0"
#__maintainer__ = "BEMOSS Team"
#__email__ = "aribemoss@gmail.com"
#__website__ = "www.bemoss.org"
#__created__ = "2014-09-12 12:04:50"
#__lastUpdated__ = "2016-03-14 11:23:33"

**/
var Is_power_on = true;
var Is_device_name = false;
// //Modify status	 when clicked
// $( "#light_on" ).click(function() {
// 	if ($("#light_on").css('background-color') == "green") {
// 	} else {
// 		$(this).css('background-color','green');
// 		$("#light_off").css('background-color','rgba(222, 222, 222, 0.55)');
// 		status = 'ON';
//         $('#brightness').slider('value', '100');
//         $('#brightness').slider('enable');
//         $('#brightness_value').val('100%');
// 	}
// });
//
// $( "#light_off" ).click(function() {
// 	if ($("#light_off").css('background-color') == "green") {
// 	} else {
// 		$(this).css('background-color','green');
// 		$("#light_on").css('background-color','rgba(222, 222, 222, 0.55)');
// 		status = 'OFF';
//         $('#brightness').slider('value', '0');
//         $('#brightness').slider('disable');
//         $('#brightness_value').val('0%');
// 	}
// });
// $(function() {
//
//     $("#brightness").slider({
//         value: brightness,
//         orientation: "horizontal",
//         range: "min",
//         animate: true,
//         min: 0,
//         max: 100,
//         slide: function (event, ui) {
//             $("#brightness_value").val(ui.value + "%");
//         }
//     });
//
//
//     $("#brightness_value").val($("#brightness").slider("value") + "%");
//     $(".slider").slider("float");
//
//
//     if (_type == '2WL') {
//         $('#brightness').slider("disable");
//         $("#brightness_value").val('');
//         $('#dim_container').css('background-color', 'rgba(255, 255, 255, 0.4)');
//     }
//
//
//     if (_type == '2HUE') {
//         $('#color_container').show();
//         if (role != 'tenant') {
//             $('.color-box').colpick({
//                 colorScheme:'dark',
//                 layout:'rgbhex',
//                 color:color,
//                 submit:0,
//                 onChange:function(hsb,hex,rgb,el) {
//                     $(el).css('background-color', 'rgb('+rgb.r+','+rgb.g+','+rgb.b+')');
//                 }
//             })
//             .css('background-color', color);
//         } else {
//             $('#color_container').css('background-color', color);
//         }
//     } else {
//         $('#color_container').css('background-color','rgba(255, 255, 255, 0.4)');
//     }
//
//      if (role == 'tenant') {
//          $('#brightness').slider("disable");
//
//     }
// });
          function startTime() {
            var now = new Date();
            var monthNames = [
              "January", "February", "March",
              "April", "May", "June", "July",
              "August", "September", "October",
              "November", "December"
            ];

            var date = new Date();
            var day = now.getDate();
            var monthIndex = now.getMonth();
            var year = now.getFullYear();

            var h = now.getHours();
            var m = now.getMinutes();
            var s = now.getSeconds();
            var ampm = h >= 12 ? 'PM' : 'AM';
            h = h % 12;
            h = h ? h : 12;
            h = checkTime(h);
            m = checkTime(m);
            s = checkTime(s);
            $('.current_time').html(monthNames[monthIndex] + " " + day + ", " + year + " " + h + ":" + m + ":" + s + " " + ampm);
            var t = setTimeout(startTime, 500);
          }
          function checkTime(i) {
            if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
            return i;
          }

          function update_Username(Username) {
            $("#Username").text(String(Username));
          }

          function update_Cur_rate(Cur_rate) {
            $("#Cur_rate").text(String(Cur_rate));
            $("#Cur_rate2").text(String(Cur_rate));
          }
         function setB(amount) {
             //softSlider.noUiSlider.set(amount);
             //alert(this.id);
             console.log(this.id);
         }
         function setMode()
         {
             //alert(this.id);
             console.log(this.id);

         }

function hexToRgb(hex) {
    // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function(m, r, g, b) {
        return r + r + g + g + b + b;
    });

    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}
function setColor(color, Human) {
    var fan = 1;
    console.log(this.id);
    if (this.id = "device_fs_auto") {
        fan = 0;
    } else if (this.id = "device_fs_auto") {
        fan = 1;

    } else if (this.id = "device_fs_low") {
        fan = 1;

    } else if (this.id = "device_fs_medium") {
        fan = 1;

    } else if (this.id = "device_fs_medium") {
        fan = 1;

    }
}


function color() {
        console.log("color was change")


}

$( document ).ready(function() {
    $.csrftoken();

    startTime();
    setValue();
    //renderChart();
    $('#log').DataTable({
        "order": [
            [0, "desc"]
        ]
    });

   $('.device_fs').on("click", function () {
       console.log(this.id);

   })
    $('#device_power_disp').on("click", function () {
        console.log("Powr SW");
        test_values = {};
        if (Is_power_on) {
            test_values["status"] = "OFF";
        } else {
            test_values["status"] = "ON";
        }
        test_values["device_info"] = ["999", "airconditioner", mac_address];
        //alert(test_values['stautss']);
        submit_air_data(test_values);
    });
    $('.btc').on("click", function () {
        console.log(this.id);
    });
});

    var ws = new WebSocket("ws://" + window.location.host + "/socket_airconditioner");

     ws.onopen = function () {
         ws.send("WS Air connected");
         console.log("open Air Socket");
     };


     ws.onmessage = function (event) {
         var _data = event.data.trim();
         _data = $.parseJSON(_data);
         var topic = _data['topic'];
         var msg = $.parseJSON(_data['message']);
         console.log(msg);

        if (msg['macaddress'] == mac_address){
             if (Is_device_name)
             {

             } else {
                 $('#device_name').html(': ' + msg['device_id']);
                 Is_device_name = true;

             }
            $('#device_set_temp').html(msg['set_temperature']);
            $
              if (msg['status'] == "ON")
             {
                 Is_power_on = true;
                 $('#device_power_disp').html("ON");
                 console.log("Device status:" + msg['status'] )
             } else if (msg['status'] == "OFF")
             {
                 console.log("Device status:" + msg['status'] )
                 Is_power_on = false;
                 $('#device_power_disp').html("OFF");
             }
             if (msg['mode'] == "Cool")
             {
                 $('.device_mode').addClass( "btn-outline" );
                 $('#device_mode_cool').removeClass( "btn-outline" );
             } else if (msg['mode'] == "Fan")
             {
                 $('.device_mode').addClass( "btn-outline" );
                 $('#device_mode_fan').removeClass( "btn-outline" );
             } else if (msg['mode'] == "Dry")
             {
                 $('.device_mode').addClass( "btn-outline" );
                 $('#device_mode_dry').removeClass( "btn-outline" );
             } else if (msg['mode'] == "Auto")
             {
                 $('.device_mode').addClass( "btn-outline" );
                 $('#device_mode_auto').removeClass( "btn-outline" );
             }
             if (msg['fan_speed'] == 0)
             {
                 $('.device_fs').addClass( "btn-outline" );
                 $('#device_fs_auto').removeClass( "btn-outline" );
             } else if (msg['fan_speed'] == 1)
             {
                 $('.device_fs').addClass( "btn-outline" );
                 $('#device_fs_low').removeClass( "btn-outline" );
             } else if (msg['fan_speed'] == 2)
             {
                 $('.device_fs').addClass( "btn-outline" );
                 $('#device_fs_medium').removeClass( "btn-outline" );
             } else if (msg['fan_speed'] == 3)
             {
                 $('.device_fs').addClass( "btn-outline" );
                 $('#device_fs_high').removeClass( "btn-outline" );
             } else if (msg['fan_speed'] == 4)
             {
                 $('.device_fs').addClass( "btn-outline" );
                 $('#device_fs_turbo').removeClass( "btn-outline" );
             }
        }
         //console.log(_data['message'])

     };
    // var ws_plug = new WebSocket("ws://" + window.location.host + "/socket_plugload");
    //
    //  ws_plug.onopen = function () {
    //      ws.send("WS Plug opened from html page");
    //  };
    //
    //  ws_plug.onmessage = function (event) {
    //      var _data = event.data.trim();
    //      _data = $.parseJSON(_data);
    //      var topic = _data['topic'];
    //      var msg = $.parseJSON(_data['message']);
    //
    //      //console.log(_data['message'])
    //      console.log('status' + msg['status']);
    //      Is_human_click = false;
    //      if (msg['status'] == "ON") {
    //          console.log("Plug status ON")
    //          $('#sw_status_p1').html("On")
    //
    //
    //      } else if (msg['status'] == "OFF") {
    //          $('#sw_status_p1').html("Off")
    //          console.log("Plug status OFF")
    //
    //      }
    //      var topic = false;
    //      // ["", "agent", "ui", device_type, command, building_name, zone_id, agent_id]
    //      if (topic) {
    //          topic = topic.split('/');
    //          console.log(topic);
    //
    //      }
    //  }
    // // function change_lighting_values(data) {
    //     if (data.status == 'ON') {
    //         $("#light_on").css('background-color', 'green');
    //         $("#light_off").css('background-color', 'rgba(222, 222, 222, 0.55)');
    //         if (data.brightness) {
    //             if ($("#brightness").slider("option", "disabled", true) && (role != 'tenant')) {
    //                 $('#brightness').slider('enable');
    //             }
    //         }
    //         status = 'ON';
		// } else {
		// 	$("#light_off").css('background-color','green');
		// 	$("#light_on").css('background-color','rgba(222, 222, 222, 0.55)');
    //         status = 'OFF';
    //         $('#brightness').slider('disable');
		// }
    //
    //     if (data.brightness) {
    //         $('#brightness').slider({ value: data.brightness });
    //         $("#brightness_value").val(data.brightness + "%");
    //     }
    //
    //
    //     if (data.color && _type == '2HUE') {
    //         var _color = data.color;
    //         _color = _color.toString(); //should be in hex #rrggbb format
    //         $('.color-box').colpick({ color: _color });
    //         $('.color-box').css('background-color', _color);
    //     }
    // }

function submit_air_data(values) {
    // topic ="ui/agent/lighting/update/bemoss/999/2HUE0017881cab4b";
    console.log("Method  " +  values.method + "  Vales " + values.value);

    var jsonText = JSON.stringify(test_values);
    console.log(jsonText);
	$.ajax({
		  url : '/update_airconditioner/',
		  type: 'POST',
		  data: jsonText,
		  dataType: 'json',
		  success : function(data) {
		     // change_lighting_values(data)
			//lighting_data_updated();
		  	/*$('.bottom-right').notify({
		  	    message: { text: 'Your settings will be updated shortly' },
		  	    type: 'blackgloss'
		  	  }).show();*/
		  },
		  error: function(data) {
              // submit_lighting_data(values);
			  $('.bottom-right').notify({
			  	    message: { text: 'Something went wrong when submitting the data. Please try again.' },
			  	    type: 'blackgloss'
			  	}).show();
		  }
		 });
}

