const { defineConfig } = require('@vue/cli-service')
module.exports = {
  pages: {
    calendar: {
      // entry for the page
      entry: 'src/pages/calendar/main.js',
      // the source template
      template: 'public/index.html',
      title: 'Calendar Page',
      // chunks to include on this page, by default includes
      // extracted common chunks and vendor chunks.
      chunks: ['chunk-vendors', 'chunk-common', 'calendar']
    },

    deadlines: {
      entry: 'src/pages/deadlines/main.js',
      template: 'public/index.html',
      title: 'Deadlines Page',
      chunks: ['chunk-vendors', 'chunk-common', 'deadlines']
    },

    login: {
      entry: 'src/pages/login/main.js',
      template: 'public/index.html',
      title: 'Login Page',
      chunks: ['chunk-vendors', 'chunk-common', 'login']
    },

    profile: {
      entry: 'src/pages/profile/main.js',
      template: 'public/index.html',
      title: 'Profile Page',
      chunks: ['chunk-vendors', 'chunk-common', 'profile']
    },

    settings: {
      entry: 'src/pages/settings/main.js',
      template: 'public/index.html',
      title: 'Settings Page',
      chunks: ['chunk-vendors', 'chunk-common', 'settings']
    },

  }
}