import * as cookie from './cookie'
import download from './download'

Object.assign(window, cookie)

window.download = download
