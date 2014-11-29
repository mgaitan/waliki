<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns="http://www.w3.org/1999/xhtml">

<xsl:import href="resource:templates/reST.xsl" />

<xsl:template match="/" name="main">
<html>
  <head>
    <title><xsl:value-of select="/document/@title"/></title>
    <meta name="generator" content="Hovercraft! via Waliki"/>
    <xsl:if test="/document/author">
        <!-- Author is a child to the document, everything else become attributes -->
      <meta name="author">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/author" />
        </xsl:attribute>
      </meta>
    </xsl:if>
    <xsl:if test="/document/@description">
      <meta name="description">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/@description" />
        </xsl:attribute>
      </meta>
    </xsl:if>
    <xsl:if test="/document/@keywords">
      <meta name="keywords">
        <xsl:attribute name="content">
          <xsl:value-of select="/document/@keywords" />
        </xsl:attribute>
      </meta>
    </xsl:if>

    <link rel="stylesheet" href="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/css/hovercraft.css" media="all"></link>
    <link rel="stylesheet" href="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/css/impressConsole.css" media="all"></link>
    <link rel="stylesheet" href="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/css/highlight.css" media="all"></link>

    <link rel="stylesheet" href="//github.com/regebro/hovercraft/blob/master/docs/examples/hovercraft.css" media="screen,projection"></link>

    <xsl:for-each select="/document/templateinfo/header/css">
        <link rel="stylesheet">
            <xsl:copy-of select="@*"/>
        </link>
    </xsl:for-each>

  </head>
  <body class="impress-not-supported">

    <xsl:for-each select="/document">
      <div id="impress">
        <xsl:if test="@data-transition-duration">
          <xsl:attribute name="data-transition-duration">
            <xsl:value-of select="@data-transition-duration" />
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@auto-console">
          <xsl:attribute name="auto-console">
            <xsl:value-of select="@auto-console" />
          </xsl:attribute>
        </xsl:if>
        <xsl:for-each select="step">
          <div class="step">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates />
          </div>
        </xsl:for-each>
      </div>
    </xsl:for-each>

    <div id="hovercraft-help">
      <xsl:if test="/document/@skip-help">
        <xsl:attribute name="class">hide</xsl:attribute>
      </xsl:if>
      <table>
        <tr><th>Space</th><td>Forward</td></tr>
        <tr><th>Right, Down, Page Down</th><td>Next slide</td></tr>
        <tr><th>Left, Up, Page Up</th><td>Previous slide</td></tr>
        <tr><th>P</th><td>Open presenter console</td></tr>
        <tr><th>H</th><td>Toggle this help</td></tr>
      </table>
    </div>


    <script type="text/javascript" src="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/js/impress.js"></script>
    <script type="text/javascript" src="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/js/impressConsole.js"></script>
    <script type="text/javascript" src="//cdn.rawgit.com/regebro/hovercraft/master/hovercraft/templates/default/js/hovercraft.js"></script>

</body>
</html>
</xsl:template>

</xsl:stylesheet>
