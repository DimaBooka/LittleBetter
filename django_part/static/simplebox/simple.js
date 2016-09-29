/**
 * Created by user on 29.09.16.
 */
(function(){
    var boxes=[],els,i,l;
    if(document.querySelectorAll){
        els=document.querySelectorAll('a[rel=simplebox]');
        Box.getStyles('simplebox_css','/static/simplebox/simplebox.css');
        Box.getScripts('simplebox_js','/static/simplebox/simplebox.js',function(){
            simplebox.init();
            for(i=0,l=els.length;i<l;++i)
                simplebox.start(els[i]);
                simplebox.start('a[rel=simplebox]');
        });
    }
})();