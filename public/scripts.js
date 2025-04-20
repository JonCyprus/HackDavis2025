$(document).ready(function() {
  var app = {
    settings: {
      container: $('.calendar'),
      calendar: $('.front'),
      days: $('.weeks span'),
      form: $('.back'),
      input: $('.back input'),
      buttons: $('.back button')
    },
  
    init: function() {
      instance = this;
      settings = this.settings;
      this.bindUIActions();
    },
  
    swap: function(currentSide, desiredSide) {
      settings.container.toggleClass('flip');
  
      currentSide.fadeOut(900);
      setTimeout(function() {
        desiredSide.fadeIn(900);
      }, 900);
    },
  
    bindUIActions: function() {
      settings.days.on('click', function() {
        instance.swap(settings.calendar, settings.form);
        settings.input.focus();
      });
  
      settings.buttons.on('click', function() {
        instance.swap(settings.form, settings.calendar);
      });
    }
  };
  
  app.init();

  // Update current date
  const today = moment();
  $('.current-date h1:first').text(today.format('dddd Do'));
  $('.current-date h1:last').text(today.format('MMMM YYYY'));
  
  // Update info date
  $('.info-date span').text(today.format('MMM Do, YYYY'));
  $('.info-time span').text(today.format('h:mm A'));
});
  