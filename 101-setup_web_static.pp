# setup.pp

# Ensure nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure nginx service is running and enabled
service { 'nginx':
  ensure     => running,
  enable     => true,
  subscribe  => File['/etc/nginx/sites-available/default'],
}

# Ensure the /data/ directory exists
file { '/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Ensure the /data/web_static/ directory exists
file { '/data/web_static/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Ensure the /data/web_static/releases/ directory exists
file { '/data/web_static/releases/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Ensure the /data/web_static/shared/ directory exists
file { '/data/web_static/shared/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Ensure the /data/web_static/releases/test/ directory exists
file { '/data/web_static/releases/test/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => '<html>
  <head>
  </head>
  <body>
    Hello World
  </body>
</html>',
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Update the Nginx configuration to serve the content
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('nginx/default.erb'),
  notify  => Service['nginx'],
}

# Ensure the template for nginx configuration
file { 'nginx/default.erb':
  ensure => file,
  path   => '/etc/puppetlabs/code/environments/production/modules/nginx/templates/default.erb',
  content => '
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
}',
}

