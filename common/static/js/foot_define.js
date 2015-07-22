(function ($) {
  $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
    if (!csrfSafeMethod(options.type) && sameOrigin(options.url)) {
      if (typeof(options.headers) == 'undefined') {
        options.headers = {};
      }
      options.headers["X-CSRFToken"] = $.cookie('csrftoken');
    }
  });
})(jQuery);

FOOT_DONE = true;
