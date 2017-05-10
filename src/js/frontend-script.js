const tagsInput = function ($) {
  const engine = new Bloodhound({
    remote: {
      url: 'http://127.0.0.1:8000/api/keywords/?query=%QUERY&format=json'
    }
  });

  $('#id_keywords').tokenfield({});

};

const wysiwygInit = function ($) {
  tinymce.init({
    selector: '.wysiwyg',
    plugins: 'link paste autoresize',
    valid_elements: 'p[style],span[style],br,strong/b,em/i,u,a[href|title|style|alt|target=_blank],ul,ol,li',
    valid_styles: {
      p: 'font-weight,text-decoration',
      span: 'font-weight,text-decoration',
      a: 'font-weight,text-decoration'
    },
    statusbar: false,
    menubar: false,
    toolbar: 'bold italic underline | bullist numlist | link',
    autoresize_bottom_margin: 10
  });
};

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    tagsInput($);
    wysiwygInit();
  });
}
