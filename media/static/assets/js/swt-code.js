$(document).ready(function() {		
	
	// Scripts for My Workouts
	$("#btn-add-cardio").click(function(){
		$("#id_style").val("Cardio Workout");
		$("#btn-add-cardio").addClass("disabled");
		$("#btn-add-weights").removeClass("disabled");
		$(".formfield-b").removeClass("hidden");
		$(".formfield-c").removeClass("hidden");
		$(".formfield-w").addClass("hidden");
	});

	$("#btn-add-weights").click(function(){
		$("#id_style").val("Weights Workout");
		$("#btn-add-weights").addClass("disabled");
		$("#btn-add-cardio").removeClass("disabled");
		$(".formfield-b").removeClass("hidden");
		$(".formfield-w").removeClass("hidden");
		$(".formfield-c").addClass("hidden");
	});

	$("#btn-cancel-workout").click(function(){
		$("#id_style").val("");
		$("#btn-add-weights").removeClass("disabled");
		$("#btn-add-cardio").removeClass("disabled");
		$(".formfield-b").addClass("hidden");
		$(".formfield-w").addClass("hidden");
		$(".formfield-c").addClass("hidden");
	});
	
	
	// Scripts for Machine Booking Today
	$("#id_machine_name").on('change',function(){
		var sel_machine= $("#id_machine_name").val();
		var prefix="div-" 
		if (sel_machine=="treadmill"){
			$("#div-rowing-time").addClass("hidden");
			$("#div-stairs-time").addClass("hidden");
			$("#div-treadmill-time").removeClass("hidden");
			$("#div-booking-submit").removeClass("hidden");
		}

		if (sel_machine=="stairs"){
			$("#div-treadmill-time").addClass("hidden");
			$("#div-rowing-time").addClass("hidden");
			$("#div-stairs-time").removeClass("hidden");
			$("#div-booking-submit").removeClass("hidden");
		}

		if (sel_machine=="rowing"){
			$("#div-treadmill-time").addClass("hidden");
			$("#div-stairs-time").addClass("hidden");
			$("#div-rowing-time").removeClass("hidden");
			$("#div-booking-submit").removeClass("hidden");
		}
	});
		
	// Script for Machine Booking Tomorrow
	$("#id_machine_name_tmr").on('change',function(){
		var sel_machine= $("#id_machine_name_tmr").val();
		var prefix="div-"
		if (sel_machine=="treadmill"){
			$("#div-rowing-time-tmr").addClass("hidden");
			$("#div-stairs-time-tmr").addClass("hidden");
			$("#div-treadmill-time-tmr").removeClass("hidden");
			$("#div-booking-submit-tmr").removeClass("hidden");
		}

		if (sel_machine=="stairs"){
			$("#div-treadmill-time-tmr").addClass("hidden");
			$("#div-rowing-time-tmr").addClass("hidden");
			$("#div-stairs-time-tmr").removeClass("hidden");
			$("#div-booking-submit-tmr").removeClass("hidden");
		}

		if (sel_machine=="rowing"){
			$("#div-treadmill-time-tmr").addClass("hidden");
			$("#div-stairs-time-tmr").addClass("hidden");
			$("#div-rowing-time-tmr").removeClass("hidden");
			$("#div-booking-submit-tmr").removeClass("hidden");
		}
	});





});

