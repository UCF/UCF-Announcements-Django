function tagsInput($) {
  const engine = new Bloodhound({
    datumTokenizer: (datum) => {
      return Bloodhound.tokenizers.whitespace(datum.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
      url: `${ANNOUNCEMENTS_CONST.KEYWORDS_API}?s=%QUERY&format=json`,
      wildcard: '%QUERY'
    }
  });

  engine.initialize();

  const $tf = $('#id_keywords').tokenfield({
    typeahead: [null, {
      source: engine.ttAdapter(),
      displayKey: 'name'
    }]
  });

  $('#id_keywords-tokenfield').on('typeahead:selected', (event, obj) => {
    $tf.tokenfield('createToken', obj.name);
  });
}

function wysiwygInit() {
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
}

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    tagsInput($);
    wysiwygInit();
  });
}
