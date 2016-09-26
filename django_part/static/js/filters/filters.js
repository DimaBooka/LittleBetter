/**
 * Created by booka on 25.09.16.
 */
linksApp.filter('onlyDone', function () {
  return function (items) {
    var done = [];
    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      if ( item.status == "done") {
        done.push(item);
      }
    }
    return done;
  };
});

linksApp.filter('nonSpace', function () {
  return function (item) {
    for (var i=0; i<item.length; i++){
        item = item.replace(' ', '_');
    }
    return item;
  };
});