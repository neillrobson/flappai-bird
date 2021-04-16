function getCookie (cname) {
  const name = cname + '='
  const ca = document.cookie.split(';')
  for (let i = 0; i < ca.length; i++) {
    const c = ca[i].trim()
    if (c.indexOf(name) === 0) return c.substring(name.length, c.length)
  }
  return ''
}

function setCookie (cname, cvalue, exdays) {
  const d = new Date()
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))
  const expires = 'expires=' + d.toGMTString()
  document.cookie = cname + '=' + cvalue + '; ' + expires + '; SameSite=Strict'
}

function setObject (cname, obj, exdays) {
  setCookie(cname, btoa(JSON.stringify(obj)), exdays)
}

function getObject (cname) {
  const str = getCookie(cname)
  if (str !== '') {
    return JSON.parse(atob(str))
  }
  return {}
}

function clearAllCookies () {
  const cookies = document.cookie.split('; ')
  for (let c = 0; c < cookies.length; c++) {
    const d = window.location.hostname.split('.')
    while (d.length > 0) {
      const cookieBase = encodeURIComponent(cookies[c].split(';')[0].split('=')[0]) + '=; SameSite=Strict; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path='
      const p = location.pathname.split('/')
      document.cookie = cookieBase + '/'
      while (p.length > 0) {
        document.cookie = cookieBase + p.join('/')
        p.pop()
      };
      d.shift()
    }
  }
}

export { getCookie, setCookie, clearAllCookies, setObject, getObject }
