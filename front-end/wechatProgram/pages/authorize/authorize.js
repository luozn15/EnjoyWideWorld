
var the_url = 'http://wangtong15.com:20001'
const app = getApp();
Page({
  data: {
    //判断小程序的API，回调，参数，组件等是否在当前版本可用。
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  onLoad: function () {
    var that = this;
    wx.login({
      success(res) {
        if (res.code) {
          console.log(res.code)
          // 发起网络请求
          wx.request({
            url: the_url + '/user/openid',
            data: {
              code: res.code
            },
            header:{
              'content-type': 'application/x-www-form-urlencoded'
            },
            method: "POST",
            success(res) {
              console.log(res)
              app.globalData.openid = res.data.openid
            }
          })
        }
      }
    })
    // 查看是否授权
    wx.getSetting({
      success: function (res) {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: function (res) {
              //从数据库获取用户信息
              that.queryUsreInfo();
              //用户已经授权过
              wx.switchTab({
                url: '/pages/map/map'
              })
            }
          });
        }
      },
    })
  },
  bindGetUserInfo: function (e) {
    if (e.detail.userInfo) {
      //用户按了允许授权按钮
      var that = this;
      app.globalData.userInfo = e.detail.userInfo;
      //插入登录的用户的相关信息到数据库
      wx.request({
        url: the_url + '/user/add',
        data: {
          wechatId: app.globalData.openid,
          nickname: e.detail.userInfo.nickName,
          avatarurl: e.detail.userInfo.avatarUrl
        },
        header: {
          'content-type': 'application/x-www-form-urlencoded'
        },
        success: function (res) {
          //从数据库获取用户信息
          // that.queryUsreInfo();
          console.log("插入小程序登录用户信息成功！");
        }
      });
      //授权成功后，跳转进入小程序首页
      wx.switchTab({
        url: '/pages/map/map'
      })
    } else {
      //用户按了拒绝按钮
      wx.showModal({
        title: '警告',
        content: '您点击了拒绝授权，将无法进入小程序，请授权之后再进入!!!',
        showCancel: false,
        confirmText: '返回授权',
        success: function (res) {
          if (res.confirm) {
            console.log('用户点击了“返回授权”')
          }
        }
      })
    }
    console.log(app.globalData.latitude),
    console.log(app.globalData.longitude)
  },
  //获取用户信息接口
  queryUsreInfo: function () {
    wx.request({
      url: app.globalData.urlPath + 'user/userInfo',
      data: {
        openid: app.globalData.openid
      },
      header: {
        'content-type': 'application/json'
      },
      success: function (res) {
        app.globalData.userInfo = res.data;
      }
    }) ;
  },

})