> 来源：[https://developers-watch.vivo.com.cn/reference/perf-guide/perf-data/](https://developers-watch.vivo.com.cn/reference/perf-guide/perf-data/)
> 更新时间：2025/04/27 11:06:02

# 响应式数据优化

蓝河框架基于 Proxy 实现响应式追踪机制，data 对象中的每个属性都会创建监听代理。优化数据层可显著降低内存消耗，提升渲染速度。

## 消除冗余响应式数据

**推荐级别：强烈**

未使用的响应式数据仍会触发依赖收集，导致内存占用增加。

**优化方案**

- 采用普遍变量声明非响应式数据
**反例 1**

```html
<template>
  <text>{{a}}</text>
</template>

<script>
  export default {
    data: {
      a: 'hello',
      b: 'world',
    },
    onInit() {
      this.a = this.a + this.b
    },
  }
</script>
```

**正例 1**

```html
<template>
  <text>{{a}}</text>
</template>

<script>
  const b = 'world'
  export default {
    data: {
      a: 'hello',
    },
    onInit() {
      this.a = this.a + b
    },
  }
</script>
```

**反例 2**

```html
<template>
  <list>
    <list-item for="{{list}}">
      <text>{{ $item.name }}</text>
      <image src="{{ $item.icon }}"></image>
    </list-item>
  </list>
</template>

<script>
  const getSportsList = () => {
    return [
      {
        name: 'Football',
        description: 'A team sport played with ...',
        category: 'Team Sports',
        icon: 'football.png',
      },
      {
        name: 'Basketball',
        description: 'A team sport in which two teams, ...',
        category: 'Team Sports',
        icon: 'basketball.png',
      },
      {
        name: 'Tennis',
        description: 'A racket sport that can be ...',
        category: 'Individual Sports',
        icon: 'tennis.png',
      },
    ]
  }
  export default {
    data: {
      sports: [],
    },
    onInit() {
      this.sports = getSportsList()
    },
  }
</script>
```

**正例 2**

```html
<template>
  <list>
    <list-item for="{{list}}">
      <text>{{ $item.name }}</text>
      <image src="{{ $item.icon }}"></image>
    </list-item>
  </list>
</template>

<script>
  const getSportsList = () => {
    return [
      {
        name: 'Football',
        description: 'A team sport played with ...',
        category: 'Team Sports',
        icon: 'football.png',
      },
      {
        name: 'Basketball',
        description: 'A team sport in which two teams, ...',
        category: 'Team Sports',
        icon: 'basketball.png',
      },
      {
        name: 'Tennis',
        description: 'A racket sport that can be ...',
        category: 'Individual Sports',
        icon: 'tennis.png',
      },
    ]
  }
  export default {
    data: {
      sports: [],
    },
    onInit() {
      this.sports = getSportsList().map((item) => ({
        name: item.name,
        icon: item.icon,
      }))
    },
  }
</script>
```

## 静态属性访问规范

**推荐级别：强烈**

**编译优化:** 动态属性访问会导致，阻碍编译时的优化分析。

**反例**

```html
<template>
  <div>
    <text>{{person.name}}</text>
    <text>{{person.location}}</text>
  </div>
</template>

<script>
  export default {
    data: {
      person: {
        name: 'Vance',
        location: 'shenzhen',
      },
    },
    onInit() {
      const location = 'location'
      this.person[location] = 'beijing'
    },
  }
</script>
```

**正例**

```html
<template>
  <div>
    <text>{{person.name}}</text>
    <text>{{person.location}}</text>
  </div>
</template>

<script>
  export default {
    data: {
      person: {
        name: 'Vance',
        location: 'shenzhen',
      },
    },
    onInit() {
      this.person.location = 'beijing'
    },
  }
</script>
```

## 数据结构层级优化

**推荐级别：鼓励**

对于动态绑定的数据，不宜嵌套层级过深，建议不超过 3 层。

**反例**

```html
<template>
  <div>
    <text>{{obj.a.name}}</text>
    <text>{{obj.b.name}}</text>
  </div>
</template>

<script>
  export default {
    data: {
      obj: {
        a: {
          name: 'name a',
        },
        b: {
          name: 'name b',
        },
      },
    },
  }
</script>
```

**正例**

```html
<template>
  <div>
    <text>{{obj.a}}</text>
    <text>{{obj.b}}</text>
  </div>
</template>

<script>
  export default {
    data: {
      obj: {
        a: 'name a',
        b: 'name b',
      },
    },
  }
</script>
```
