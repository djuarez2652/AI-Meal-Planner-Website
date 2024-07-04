/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/login.html"],
  theme: {
    extend: {},
  },
  plugins: [
      function({addUtilities}) {
        addUtilities({
          '.input-field': {
            border: '1px solid black',
            borderRadius: '5px',
            marginLeft: '10px',
          },
          '.form-group': {
            display: 'flex',
            justifyContent: 'space-between',
          },
          '.btn-div': {
            border: '1px solid black',
            width: '100%',
            backgroundColor: '#68d954',
            borderRadius: '3px',
          },
          '.btn-div:hover': {
            backgroundColor: '#57b846',
          },
          '.btn': {
            width: '100%',
            cursor: 'pointer',
          },
        })
      }
  ],
}