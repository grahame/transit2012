function searchWidget() {
    new TWTR.Widget({
      version: 2,
      type: 'search',
      search: '#venusobs',
      interval: 30000,
      title: 'Live feed',
      subject: 'Venus Transit Observations',
      width: 250,
      height: 300,
      theme: {
        shell: {
          background: '#8ec1da',
          color: '#ffffff'
        },
        tweets: {
          background: '#ffffff',
          color: '#444444',
          links: '#1985b5'
        }
      },
      features: {
        scrollbar: true,
        loop: true,
        live: true,
        behavior: 'default'
      }
    }).render().start();
}
